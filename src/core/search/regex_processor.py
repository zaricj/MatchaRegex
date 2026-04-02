import re
import mmap
import pandas as pd
from typing import Any
from pathlib import Path
from PySide6.QtCore import QObject, Signal
from core.patterns.pattern_profiles import PatternSpec


class RegexProcessorSignals(QObject):
    message_information   = Signal(str, str)
    message_warning       = Signal(str, str)
    message_critical      = Signal(str, str)
    program_output_text   = Signal(str)
    statusbar_show_message = Signal(str, int)
    progress_update       = Signal(int)
    finished              = Signal(pd.DataFrame)
 
 
class RegexSearchTask:
    # Files below this threshold are decoded fully and segmented into blocks.
    # Files at or above it are scanned in-place via mmap (bytes, never fully decoded).
    _MMAP_THRESHOLD = 200 * 1024 * 1024  # 200 MB
 
    def __init__(
        self,
        segmentation_mode: str = "Auto",
        regex_patterns: list = None,
        folder_path: Path = None,
        file_patterns: list[str] = None,
        multiline: bool = False,
        max_rows: int = 0,
        signals: RegexProcessorSignals | None = None,
    ):
        self.segmentation_mode = segmentation_mode
        self.signals           = signals or RegexProcessorSignals()
        self.regex_patterns    = regex_patterns or []
        self.folder_path       = folder_path
        self.file_patterns     = file_patterns or []
        self.multiline         = multiline
        self.max_rows          = max_rows
 
    # ------------------------------------------------------------------
    # Pattern helpers
    # ------------------------------------------------------------------
 
    def _normalize_pattern_specs(self) -> list[PatternSpec]:
        """
        Convert whatever was passed in ``regex_patterns`` into a flat list of
        ``PatternSpec`` objects.  Entries without a usable expression are
        silently skipped; entries without an explicit name fall back to the
        spec's own ``name`` field (never a synthetic ``Pattern{N}`` label).
        """
        normalized: list[PatternSpec] = []
        for pattern in self.regex_patterns:
            if isinstance(pattern, PatternSpec):
                if pattern.expression.strip():
                    normalized.append(pattern)
            elif isinstance(pattern, dict):
                expression = str(pattern.get("expression", "")).strip()
                if not expression:
                    continue
                name = str(pattern.get("name", "")).strip()
                if not name:
                    continue                    # no synthetic name — skip unnamed dicts
                normalized.append(PatternSpec(name=name, expression=expression))
            else:
                # Plain string — requires at least one named group; used as-is
                expression = str(pattern).strip()
                if expression:
                    # No name available for plain strings; they must carry named
                    # groups to produce meaningful columns.  Use the pattern text
                    # itself only as an identifier (never written to the CSV).
                    normalized.append(PatternSpec(name=expression[:60], expression=expression))
        return normalized
 
    def _base_flags(self) -> int:
        """
        re.MULTILINE is always on so ^ / $ anchor per line.
        re.DOTALL is only added when the user enables multiline mode (mmap path).
        """
        flags = re.MULTILINE
        if self.multiline:
            flags |= re.DOTALL
        return flags
 
    def _compile_str_patterns(self) -> list[tuple[PatternSpec, re.Pattern]]:
        """Compile str patterns for the segmentation path (< _MMAP_THRESHOLD)."""
        flags    = re.MULTILINE   # DOTALL unneeded — blocks are already segmented
        compiled = []
        for spec in self._normalize_pattern_specs():
            try:
                compiled.append((spec, re.compile(spec.expression, flags)))
            except re.error as exc:
                raise ValueError(f"Regex Error in '{spec.name}': {exc}") from exc
        return compiled
 
    def _compile_bytes_patterns(self) -> list[tuple[PatternSpec, re.Pattern]]:
        """Compile bytes patterns for the mmap streaming path (>= _MMAP_THRESHOLD)."""
        flags    = self._base_flags()
        compiled = []
        for spec in self._normalize_pattern_specs():
            try:
                compiled.append((spec, re.compile(spec.expression.encode("utf-8"), flags)))
            except re.error as exc:
                raise ValueError(f"Regex Error in '{spec.name}': {exc}") from exc
        return compiled
 
    # ------------------------------------------------------------------
    # File collection
    # ------------------------------------------------------------------
 
    def _collect_files(self) -> list[Path]:
        if not self.folder_path or not self.folder_path.exists():
            raise ValueError("Target folder does not exist.")
 
        if self.file_patterns and any(fp.strip() for fp in self.file_patterns):
            valid    = [fp.strip() for fp in self.file_patterns if fp.strip()]
            file_set: set[Path] = set()
            for p in valid:
                file_set.update(self.folder_path.glob(p))
        else:
            file_set = set(self.folder_path.glob("*.*"))
 
        return sorted(file_set, key=lambda x: x.name)
 
    # ------------------------------------------------------------------
    # Per-file processing
    # ------------------------------------------------------------------
 
    def _match_to_row(
        self,
        match: re.Match,
        filepath: Path,
        decode: bool = False,
    ) -> dict[str, Any]:
        """
        Build a result row from a single regex match.
 
        * Named groups  → one column per group name (value decoded if bytes).
        * No named groups → a single ``Match`` column with the full match text.
 
        ``File`` is always included as the first column.
        """
        row: dict[str, Any] = {"File": filepath.name}
 
        groupdict = match.groupdict()
        if groupdict:
            for key, value in groupdict.items():
                if decode and isinstance(value, (bytes, bytearray)):
                    row[key] = value.decode("latin-1", "replace") if value is not None else ""
                else:
                    row[key] = value if value is not None else ""
        else:
            raw = match.group(0)
            row["Match"] = raw.decode("latin-1", "replace") if (decode and isinstance(raw, (bytes, bytearray))) else raw
 
        return row
 
    def _process_with_segmentation(
        self,
        filepath: Path,
        str_patterns: list[tuple[PatternSpec, re.Pattern]],
    ) -> list[dict[str, Any]]:
        """
        For files *under* _MMAP_THRESHOLD.
 
        Reads the whole file once via mmap, decodes it, then segments it into
        logical blocks (lines / timestamps / exceptions).  Each block is then
        searched with every compiled pattern.  Named groups become columns;
        unnamed matches fall back to a ``Match`` column.
 
        The ``ParserEngine`` is intentionally *not* used here — headers come
        from regex group names, not from engine-defined field names.
        """
        from core.search.segmenters import (
            detect_segmenter,
            LineSegmenter,
            ExceptionSegmenter,
            TimestampSegmenter,
        )
 
        results: list[dict[str, Any]] = []
        try:
            with open(filepath, "rb") as fh:
                with mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    text = mm.read().decode("latin-1", "replace")
 
            mode = self.segmentation_mode
            if mode == "Timestamp":
                segmenter = TimestampSegmenter()
            elif mode == "Exception":
                segmenter = ExceptionSegmenter()
            elif mode == "Line":
                segmenter = LineSegmenter()
            else:                          # "Auto" or anything else
                segmenter = detect_segmenter(text)
 
            blocks = segmenter.split(text)
 
            for block in blocks:
                for _spec, compiled in str_patterns:
                    for match in compiled.finditer(block):
                        results.append(self._match_to_row(match, filepath, decode=False))
                        if 0 < self.max_rows <= len(results):
                            return results
 
        except Exception as exc:
            self.signals.message_warning.emit(
                "Segmentation Error", f"Could not process {filepath.name}: {exc}"
            )
        return results
 
    def _process_with_mmap(
        self,
        filepath: Path,
        bytes_patterns: list[tuple[PatternSpec, re.Pattern]],
    ) -> list[dict[str, Any]]:
        """
        For files *at or above* _MMAP_THRESHOLD.
 
        Scans the raw bytes directly — the file is never fully decoded.
        Only matched slices are decoded on demand.
        """
        results: list[dict[str, Any]] = []
        try:
            with open(filepath, "rb") as fh:
                with mmap.mmap(fh.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    for _spec, compiled in bytes_patterns:
                        for match in compiled.finditer(mm):
                            results.append(self._match_to_row(match, filepath, decode=True))
                            if 0 < self.max_rows <= len(results):
                                return results
        except Exception as exc:
            self.signals.message_warning.emit(
                "Mmap Error", f"Could not process {filepath.name}: {exc}"
            )
        return results
 
    # ------------------------------------------------------------------
    # Orchestration
    # ------------------------------------------------------------------
 
    def search_files(self) -> list[dict[str, Any]]:
        files = self._collect_files()
        if not files:
            self.signals.program_output_text.emit("No files found matching patterns.")
            return []
 
        # Compile once, reuse across every file
        str_patterns   = self._compile_str_patterns()
        bytes_patterns = self._compile_bytes_patterns()
 
        all_results: list[dict[str, Any]] = []
        total = len(files)
 
        for index, filepath in enumerate(files, start=1):
            if not filepath.is_file():
                continue
 
            self.signals.program_output_text.emit(f"Scanning: {filepath.name}")
 
            if filepath.stat().st_size < self._MMAP_THRESHOLD:
                file_matches = self._process_with_segmentation(filepath, str_patterns)
            else:
                file_matches = self._process_with_mmap(filepath, bytes_patterns)
 
            all_results.extend(file_matches)
            self.signals.progress_update.emit(int((index / total) * 100))
 
            if 0 < self.max_rows <= len(all_results):
                self.signals.program_output_text.emit(
                    f"Row limit ({self.max_rows}) reached."
                )
                break
 
        return all_results
 
    def run(self) -> None:
        try:
            self.signals.program_output_text.emit("Starting Search...")
            results = self.search_files()
 
            if results:
                self.signals.program_output_text.emit(
                    f"Formatting {len(results)} matches..."
                )
                df = pd.DataFrame(results)
                df = df.fillna("").astype(str)
 
                # "File" always comes first; remaining columns sorted alphabetically
                cols = df.columns.tolist()
                head = [c for c in ["File"] if c in cols]
                body = sorted(c for c in cols if c not in head)
                df   = df[head + body]
 
                self.signals.finished.emit(df)
            else:
                self.signals.program_output_text.emit("Search finished with 0 results.")
                self.signals.finished.emit(pd.DataFrame())
 
        except Exception as exc:
            self.signals.message_critical.emit("Fatal Search Error", str(exc))
            self.signals.finished.emit(pd.DataFrame())
 
 
# ---------------------------------------------------------------------------
# Convenience wrapper — called from a Worker thread (non-blocking)
# ---------------------------------------------------------------------------
 
def run_regex_search(
    segmentation_mode: str = "Auto",
    regex_patterns: list = None,
    folder_path: Path = None,
    file_patterns: list[str] | None = None,
    multiline: bool = False,
    max_rows: int = 0,
    signals: RegexProcessorSignals | None = None,
) -> None:
    RegexSearchTask(
        segmentation_mode=segmentation_mode,
        regex_patterns=regex_patterns,
        folder_path=folder_path,
        file_patterns=file_patterns,
        multiline=multiline,
        max_rows=max_rows,
        signals=signals,
    ).run()
 