from typing import Any
import re
from pathlib import Path
from PySide6.QtCore import QObject, Signal
import pandas as pd
from core.patterns.pattern_profiles import PatternSpec


class RegexProcessorSignals(QObject):
    message_information = Signal(str, str)
    message_warning = Signal(str, str)
    message_critical = Signal(str, str)
    program_output_text = Signal(str)
    statusbar_show_message = Signal(str, int)
    progress_update = Signal(int)
    finished = Signal(pd.DataFrame)


class RegexSearchTask:
    def __init__(self, regex_patterns: list = None, folder_path: Path = None,
                 file_patterns: list[str] = None, multiline: bool = False, max_rows: int = 0,
                 signals: RegexProcessorSignals | None = None):
        self.signals = signals or RegexProcessorSignals()
        self.regex_patterns = regex_patterns if regex_patterns is not None else []
        self.folder_path = folder_path
        self.file_patterns = file_patterns if file_patterns is not None else []
        self.multiline = multiline
        self.max_rows = max_rows

    def _normalize_pattern_specs(self) -> list[PatternSpec]:
        normalized: list[PatternSpec] = []
        for index, pattern in enumerate(self.regex_patterns, start=1):
            if isinstance(pattern, PatternSpec):
                normalized.append(pattern)
            elif isinstance(pattern, dict):
                expression = str(pattern.get("expression", "")).strip()
                if expression:
                    normalized.append(
                        PatternSpec(
                            name=str(pattern.get("name", f"Pattern{index}")).strip() or f"Pattern{index}",
                            expression=expression,
                        )
                    )
            else:
                expression = str(pattern).strip()
                if expression:
                    normalized.append(
                        PatternSpec(name=f"Pattern{index}", expression=expression)
                    )
        return normalized

    def run(self):
        results: list[dict[str, Any]] = []
        try:
            results = self.search_files()

            if results:
                # Normalize results to ensure consistent keys (in background thread)
                all_keys = set()
                for result in results:
                    all_keys.update(result.keys())
                for result in results:
                    for key in all_keys:
                        if key not in result:
                            result[key] = ""
                # Create DataFrame in background thread (not main thread!)
                self.signals.program_output_text.emit(
                    f"Creating DataFrame with {len(results)} rows...")
                results_df = pd.DataFrame(results, dtype=str)
                self.signals.finished.emit(results_df)
            else:
                # Emit empty DataFrame
                self.signals.finished.emit(pd.DataFrame())

        except Exception as e:
            self.signals.message_critical.emit(
                "Search Error", f"Thread error: {str(e)}")
            self.signals.finished.emit(pd.DataFrame())

    def extract_named_groups_from_regex(self, regex_pattern: str) -> list[str]:
        """Extract named groups from regex pattern string."""
        group_pattern = r'\(\?P<(\w+)>'
        return re.findall(group_pattern, regex_pattern)

    def process_files(self, files: list[Path], compiled_patterns: list,
                      pattern_group_names: list) -> list[dict[str, Any]]:
        """Process files with compiled regex patterns."""
        total = len(files)
        # Sorts the files by name for consistent processing order
        files = sorted(files, key=lambda f: f.name)
        results = []

        # Pre-calculate column naming strategy
        all_group_names = set()
        for _pattern_spec, group_names in pattern_group_names:
            all_group_names.update(group_names)

        use_pattern_prefix = len(all_group_names) < sum(
            len(group_names) for _pattern_spec, group_names in pattern_group_names)

        col_name_maps = []
        for pattern_spec, group_names in pattern_group_names:
            if group_names:
                if use_pattern_prefix:
                    col_map = {
                        gn: f"{pattern_spec.name}_{gn}" for gn in group_names}
                else:
                    col_map = {gn: gn for gn in group_names}
            else:
                col_map = None
            col_name_maps.append((pattern_spec, col_map))

        # Batch progress updates (every 5% or every 10 files, whichever is smaller)
        progress_interval = max(1, min(10, total // 20))

        for index, filepath in enumerate(files, start=1):
            # Reduce signal emissions for speed
            if index == 1 or index % progress_interval == 0 or index == total:
                self.signals.program_output_text.emit(
                    f"Processing file: {filepath.name}")

            try:
                if not filepath.is_file() or not filepath.exists():
                    continue

                # Read file with larger buffer for better I/O performance
                with open(filepath, "r", encoding="utf-8", errors="replace", buffering=65536) as f:
                    # If multiline is enabled, read entire file at once
                    if self.multiline:
                        text = f.read()
                        # Combine all patterns into single search pass if possible
                        for compiled_regex, (pattern_spec, col_map) in zip(compiled_patterns, col_name_maps):
                            for match in compiled_regex.finditer(text):
                                result = {"File": filepath.name, "Pattern": pattern_spec.name}
                                if col_map:
                                    # Use pre-built column names
                                    groupdict = match.groupdict()
                                    for group_name, col_name in col_map.items():
                                        result[col_name] = groupdict.get(
                                            group_name) or ""
                                else:
                                    result["Match"] = match.group(0) or ""
                                results.append(result)
                                # Limit results early if max_rows is set and greater than 0
                                if self.max_rows > 0 and len(results) >= self.max_rows:
                                    self.signals.program_output_text.emit(
                                        f"Reached result limit of {self.max_rows}")
                                    return results
                    else:
                        # Line-by-line processing
                        for line in f:
                            line = line.strip()
                            if not line:
                                continue

                            for compiled_regex, (pattern_spec, col_map) in zip(compiled_patterns, col_name_maps):
                                try:
                                    for match in compiled_regex.finditer(line):
                                        result = {
                                            "File": filepath.name, "Pattern": pattern_spec.name}
                                        if col_map:
                                            groupdict = match.groupdict()
                                            for group_name, col_name in col_map.items():
                                                result[col_name] = groupdict.get(
                                                    group_name) or ""
                                        else:
                                            result["Match"] = match.group(0) or ""
                                        results.append(result)
                                        # Limit results early if max_rows is set and greater than 0
                                        if self.max_rows > 0 and len(results) >= self.max_rows:
                                            self.signals.program_output_text.emit(
                                                f"Reached result limit of {self.max_rows}")
                                            return results
                                except Exception:
                                    # Silently continue on regex errors for speed
                                    continue

            except Exception:
                # Silently continue on file errors for speed
                continue

            # Batch progress updates
            if index % progress_interval == 0 or index == total:
                progress = int((index / total) * 100)
                self.signals.progress_update.emit(progress)

        self.signals.program_output_text.emit(
            f"Processed {total} files, {len(results)} matches found")
        return results

    def limit_results(self, results: list[dict[str, Any]], max_rows: int) -> list[dict[str, Any]]:
        """Limit the number of results to max_rows."""
        if max_rows > 0 and len(results) > max_rows:
            self.signals.program_output_text.emit(
                f"Limiting results to first {max_rows} rows")
            return results[:max_rows]
        return results

    def search_files(self) -> list[dict[str, Any]]:
        """Search files using regex patterns."""
        if not self.folder_path or not self.folder_path.exists():
            raise ValueError("Invalid or non-existent folder path")

        if not self.regex_patterns:
            raise ValueError("No regex patterns provided. Exiting.")

        # More efficient file gathering
        files = []
        if self.file_patterns and any(fp.strip() for fp in self.file_patterns):
            valid_patterns = [fp.strip()
                              for fp in self.file_patterns if fp.strip()]
            # Use set to avoid duplicates when multiple patterns match same file
            file_set = set()
            for pattern in valid_patterns:
                file_set.update(self.folder_path.glob(pattern))
            files = list(file_set)
            self.signals.program_output_text.emit(
                f"Found {len(files)} files using patterns: {valid_patterns}")
        else:
            files = list(self.folder_path.glob('*.*'))
            self.signals.program_output_text.emit(
                f"Found {len(files)} files (all files)")

        if not files:
            self.signals.program_output_text.emit("No files found to search")
            return []

        # Pre-compile all patterns once
        compiled_patterns = []
        pattern_group_names = []

        flags = re.MULTILINE if self.multiline else 0
        pattern_specs = self._normalize_pattern_specs()
        for pattern_spec in pattern_specs:
            try:
                compiled = re.compile(pattern_spec.expression, flags)
                group_names = self.extract_named_groups_from_regex(pattern_spec.expression)
                compiled_patterns.append(compiled)
                pattern_group_names.append((pattern_spec, group_names))
            except re.error as e:
                raise ValueError(f"Invalid regex pattern '{pattern_spec.name}': {e}")

        self.signals.program_output_text.emit("Starting file processing")

        results = self.process_files(
            files, compiled_patterns, pattern_group_names)

        return results


def run_regex_search(regex_patterns: list = None, folder_path: Path = None,
                     file_patterns: list[str] | None = None, multiline: bool = False,
                     max_rows: int = 0, signals: RegexProcessorSignals | None = None):
    task = RegexSearchTask(
        regex_patterns=regex_patterns,
        folder_path=folder_path,
        file_patterns=file_patterns,
        multiline=multiline,
        max_rows=max_rows,
        signals=signals,
    )
    task.run()
