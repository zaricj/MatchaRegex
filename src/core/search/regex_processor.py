import re
import mmap
import pandas as pd
from typing import Any
from pathlib import Path
from PySide6.QtCore import QObject, Signal
from core.patterns.pattern_profiles import PatternSpec


class RegexProcessorSignals(QObject):
    message_information = Signal(str, str)
    message_warning   = Signal(str, str)
    message_critical  = Signal(str, str)
    program_output_text = Signal(str)
    statusbar_show_message = Signal(str, int)
    progress_update = Signal(int)
    finished = Signal(pd.DataFrame)


class RegexSearchTask:
    # Threshold: below this, decode to str and use segmentation/ParserEngine.
    # Above this, stay in bytes and use mmap streaming.
    _MMAP_THRESHOLD = 200 * 1024 * 1024  # 200MB

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
        self.multiline         = multiline   # True = re.DOTALL (. crosses newlines)
        self.max_rows          = max_rows

    # ------------------------------------------------------------------
    # Pattern helpers
    # ------------------------------------------------------------------

    def _normalize_pattern_specs(self) -> list[PatternSpec]:
        normalized: list[PatternSpec] = []
        for index, pattern in enumerate(self.regex_patterns, start=1):
            if isinstance(pattern, PatternSpec):
                normalized.append(pattern)
            elif isinstance(pattern, dict):
                expression = str(pattern.get("expression", "")).strip()
                if expression:
                    normalized.append(PatternSpec(
                        name=str(pattern.get("name", f"Pattern{index}")).strip() or f"Pattern{index}",
                        expression=expression,
                    ))
            else:
                expression = str(pattern).strip()
                if expression:
                    normalized.append(PatternSpec(name=f"Pattern{index}", expression=expression))
        return normalized

    def _base_flags(self) -> int:
        """
        re.MULTILINE is always on so ^ and $ anchor per line.
        re.DOTALL (. crosses newlines) is only added when the user
        explicitly enables multiline mode — and only for the mmap path,
        where you control the pattern. The segmentation path splits into
        blocks first, so DOTALL is irrelevant there.
        """
        flags = re.MULTILINE
        if self.multiline:
            flags |= re.DOTALL
        return flags

    def _compile_str_patterns(self) -> list[tuple[PatternSpec, re.Pattern]]:
        """Compile as str patterns for the segmentation path (<200MB)."""
        flags = re.MULTILINE  # DOTALL not needed; blocks are already segmented
        compiled = []
        for spec in self._normalize_pattern_specs():
            try:
                compiled.append((spec, re.compile(spec.expression, flags)))
            except re.error as e:
                raise ValueError(f"Regex Error in '{spec.name}': {e}")
        return compiled

    def _compile_bytes_patterns(self) -> list[tuple[PatternSpec, re.Pattern]]:
        """Compile as bytes patterns for the mmap streaming path (>=200MB)."""
        flags = self._base_flags()
        compiled = []
        for spec in self._normalize_pattern_specs():
            try:
                compiled.append((spec, re.compile(spec.expression.encode("utf-8"), flags)))
            except re.error as e:
                raise ValueError(f"Regex Error in '{spec.name}': {e}")
        return compiled

    # ------------------------------------------------------------------
    # File processing
    # ------------------------------------------------------------------

    def _collect_files(self) -> list[Path]:
        if not self.folder_path or not self.folder_path.exists():
            raise ValueError("Target folder does not exist.")

        if self.file_patterns and any(fp.strip() for fp in self.file_patterns):
            valid = [fp.strip() for fp in self.file_patterns if fp.strip()]
            file_set: set[Path] = set()
            for p in valid:
                file_set.update(self.folder_path.glob(p))
        else:
            file_set = set(self.folder_path.glob("*.*"))

        return sorted(file_set, key=lambda x: x.name)

    def _process_with_segmentation(
        self, filepath: Path, str_patterns: list[tuple[PatternSpec, re.Pattern]]
    ) -> list[dict[str, Any]]:
        """
        For files under the mmap threshold.
        Decodes once, segments into blocks, then runs ParserEngine.
        str_patterns must be compiled against str (not bytes).
        """
        from core.search.segmenters import detect_segmenter, LineSegmenter, ExceptionSegmenter, TimestampSegmenter
        from core.search.parsing_engine import ParserEngine

        results = []
        try:
            with open(filepath, "rb") as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    text = mm.read().decode("latin-1", "replace")

            mode = self.segmentation_mode
            if mode == "Timestamp":
                segmenter = TimestampSegmenter()
            elif mode == "Exception":
                segmenter = ExceptionSegmenter()
            elif mode == "Line":
                segmenter = LineSegmenter()
            else:  # "Auto" or anything else
                segmenter = detect_segmenter(text)

            blocks = segmenter.split(text)

            parser = ParserEngine({spec.name: spec.expression for spec, _ in str_patterns})
            df = parser.parse(blocks)

            for _, row in df.iterrows():
                row_dict = row.to_dict()
                row_dict["File"] = filepath.name
                results.append(row_dict)
                if 0 < self.max_rows <= len(results):
                    return results

        except Exception as ex:
            self.signals.message_warning.emit(
                "Segmentation Error", f"Could not process {filepath.name}: {ex}"
            )
        return results

    def _process_with_mmap(
        self, filepath: Path, bytes_patterns: list[tuple[PatternSpec, re.Pattern]]
    ) -> list[dict[str, Any]]:
        """
        For files over the mmap threshold.
        Never decodes the full file — reads only matched slices.
        bytes_patterns must be compiled against bytes.
        """
        results = []
        try:
            with open(filepath, "rb") as f:
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    for pattern_spec, compiled_regex in bytes_patterns:
                        for match in compiled_regex.finditer(mm):
                            row: dict[str, Any] = {
                                "File": filepath.name,
                                "Pattern": pattern_spec.name,
                            }
                            groupdict = match.groupdict()
                            if groupdict:
                                for key, val_bytes in groupdict.items():
                                    row[key] = val_bytes.decode("latin-1", "replace") if val_bytes is not None else ""
                            else:
                                row["Match"] = match.group(0).decode("latin-1", "replace")

                            results.append(row)
                            if 0 < self.max_rows <= len(results):
                                return results
        except Exception as ex:
            self.signals.message_warning.emit(
                "Mmap Error", f"Could not process {filepath.name}: {ex}"
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

        # Compile once, reused across all files
        str_patterns   = self._compile_str_patterns()
        bytes_patterns = self._compile_bytes_patterns()

        all_results: list[dict[str, Any]] = []
        total = len(files)

        for index, filepath in enumerate(files, start=1):
            if not filepath.is_file():
                continue

            self.signals.program_output_text.emit(f"Scanning: {filepath.name}")

            file_size = filepath.stat().st_size
            if file_size < self._MMAP_THRESHOLD:
                file_matches = self._process_with_segmentation(filepath, str_patterns)
            else:
                file_matches = self._process_with_mmap(filepath, bytes_patterns)

            all_results.extend(file_matches)
            self.signals.progress_update.emit(int((index / total) * 100))

            if 0 < self.max_rows <= len(all_results):
                self.signals.program_output_text.emit(f"Row limit ({self.max_rows}) reached.")
                break

        return all_results

    def run(self) -> None:
        try:
            self.signals.program_output_text.emit("Starting Search...")
            results = self.search_files()

            if results:
                self.signals.program_output_text.emit(f"Formatting {len(results)} matches...")
                df = pd.DataFrame(results)
                df = df.fillna("").astype(str)

                cols = df.columns.tolist()
                head = [c for c in ["File", "Pattern"] if c in cols]
                body = sorted(c for c in cols if c not in head)
                df = df[head + body]
                self.signals.finished.emit(df)
            else:
                self.signals.program_output_text.emit("Search finished with 0 results.")
                self.signals.finished.emit(pd.DataFrame())

        except Exception as e:
            self.signals.message_critical.emit("Fatal Search Error", str(e))
            self.signals.finished.emit(pd.DataFrame())


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