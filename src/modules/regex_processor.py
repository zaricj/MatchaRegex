from typing import Any
import re
from pathlib import Path
from PySide6.QtCore import QObject, Signal, QRunnable, Slot

class RegexProcessorSignals(QObject):
    message_information = Signal(str, str)
    message_warning = Signal(str, str)
    message_critical = Signal(str, str)
    program_output_text = Signal(str)
    statusbar_show_message = Signal(str, int)
    progress_update = Signal(int)
    finished = Signal(list)

class RegexProcessorThread(QRunnable):
    def __init__(self, operation: str, regex_patterns: list = None, folder_path: Path = None, 
                file_patterns: list[str] = None, multiline: bool = False, max_rows: int = 0):
        super().__init__()
        self.signals = RegexProcessorSignals()
        self.operation = operation
        self.regex_patterns = regex_patterns if regex_patterns is not None else []
        self.folder_path = folder_path
        self.file_patterns = file_patterns if file_patterns is not None else []
        self.multiline = multiline
        self.max_rows = max_rows  # Default to 0 (no limit)
        self.setAutoDelete(True)

    @Slot()
    def run(self):
        results = []
        try:
            if self.operation == 'search_files':
                results = self.search_files()
            else:
                raise ValueError(f"Unknown operation: {self.operation}")
        except Exception as e:
            self.signals.message_critical.emit("Search Error", f"Thread error: {str(e)}")
        finally:
            self.signals.finished.emit(results)

    def extract_named_groups_from_regex(self, regex_pattern: str) -> list[str]:
        """Extract named groups from regex pattern string."""
        group_pattern = r'\(\?P<(\w+)>'
        return re.findall(group_pattern, regex_pattern)

    def process_files(self, files: list[Path], compiled_patterns: list, 
                    pattern_group_names: list) -> list[dict[str, Any]]:
        """Process files with compiled regex patterns."""
        total = len(files)
        results = []

        # Pre-calculate column naming strategy
        all_group_names = set()
        for group_names in pattern_group_names:
            all_group_names.update(group_names)
            
        use_pattern_prefix = len(all_group_names) < sum(len(gn) for gn in pattern_group_names)

        # Pre-build column name mappings to avoid repeated string formatting
        col_name_maps = []
        for pattern_idx, group_names in enumerate(pattern_group_names, 1):
            if group_names:
                if use_pattern_prefix:
                    col_map = {gn: f"Pattern{pattern_idx}_{gn}" for gn in group_names}
                else:
                    col_map = {gn: gn for gn in group_names}
            else:
                col_map = None
            col_name_maps.append((col_map, f"Pattern{pattern_idx}_Match"))

        # Batch progress updates (every 5% or every 10 files, whichever is smaller)
        progress_interval = max(1, min(10, total // 20))
        
        for index, filepath in enumerate(files, start=1):
            # Reduce signal emissions for speed
            if index == 1 or index % progress_interval == 0 or index == total:
                self.signals.program_output_text.emit(f"Processing file: {filepath.name}")
            
            try:
                if not filepath.is_file() or not filepath.exists():
                    continue

                # Read file with larger buffer for better I/O performance
                with open(filepath, "r", encoding="utf-8", errors="replace", buffering=65536) as f:
                    if self.multiline:
                        text = f.read()
                        # Combine all patterns into single search pass if possible
                        for pattern_idx, (compiled_regex, (col_map, match_col)) in enumerate(zip(compiled_patterns, col_name_maps)):
                            for match in compiled_regex.finditer(text):
                                result = {"File": filepath.name}
                                if col_map:
                                    # Use pre-built column names
                                    groupdict = match.groupdict()
                                    for group_name, col_name in col_map.items():
                                        result[col_name] = groupdict.get(group_name) or ""
                                else:
                                    result[match_col] = match.group(0) or ""
                                results.append(result)
                                # Limit results early if max_rows is set and greater than 0
                                if self.max_rows > 0 and len(results) >= self.max_rows:
                                    self.signals.program_output_text.emit(f"Reached result limit of {self.max_rows}")
                                    return results
                    else:
                        # Line-by-line processing
                        for line_number, line in enumerate(f, start=1):
                            line = line.strip()
                            if not line:
                                continue

                            for pattern_idx, (compiled_regex, (col_map, match_col)) in enumerate(zip(compiled_patterns, col_name_maps)):
                                try:
                                    for match in compiled_regex.finditer(line):
                                        result = {"File": filepath.name, "Line": line_number}
                                        if col_map:
                                            groupdict = match.groupdict()
                                            for group_name, col_name in col_map.items():
                                                result[col_name] = groupdict.get(group_name) or ""
                                        else:
                                            result[match_col] = match.group(0) or ""
                                        results.append(result)
                                        # Limit results early if max_rows is set and greater than 0
                                        if self.max_rows > 0 and len(results) >= self.max_rows:
                                            self.signals.program_output_text.emit(f"Reached result limit of {self.max_rows}")
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

        self.signals.program_output_text.emit(f"Processed {total} files, {len(results)} matches found")
        return results
    
    def limit_results(self, results: list[dict[str, Any]], max_rows: int) -> list[dict[str, Any]]:
        """Limit the number of results to max_rows."""
        if max_rows > 0 and len(results) > max_rows:
            self.signals.program_output_text.emit(f"Limiting results to first {max_rows} rows")
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
            valid_patterns = [fp.strip() for fp in self.file_patterns if fp.strip()]
            # Use set to avoid duplicates when multiple patterns match same file
            file_set = set()
            for pattern in valid_patterns:
                file_set.update(self.folder_path.glob(pattern))
            files = list(file_set)
            self.signals.program_output_text.emit(f"Found {len(files)} files using patterns: {valid_patterns}")
        else:
            files = list(self.folder_path.glob('*.*'))
            self.signals.program_output_text.emit(f"Found {len(files)} files (all files)")
            
        if not files:
            self.signals.program_output_text.emit("No files found to search")
            return []
            
        # Pre-compile all patterns once
        compiled_patterns = []
        pattern_group_names = []
        
        flags = re.MULTILINE if self.multiline else 0
        for regex in self.regex_patterns:
            try:
                compiled = re.compile(regex, flags)
                group_names = self.extract_named_groups_from_regex(regex)
                compiled_patterns.append(compiled)
                pattern_group_names.append(group_names)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern '{regex}': {e}")
        
        self.signals.program_output_text.emit("Starting file processing")
        
        results = self.process_files(files, compiled_patterns, pattern_group_names)
        
        return results