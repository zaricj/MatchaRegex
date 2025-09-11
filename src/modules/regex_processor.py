from typing import Any
import re
from pathlib import Path
from PySide6.QtCore import QObject, Signal, QRunnable, Slot
import time

class RegexProcessorSignals(QObject):
    message_information = Signal(str, str)
    message_warning = Signal(str, str)
    message_critical = Signal(str, str)
    program_output_text = Signal(str)
    statusbar_show_message = Signal(str, int)
    progress_update = Signal(int)
    finished = Signal(list)  # Changed to emit list instead of pd.DataFrame

class RegexProcessorThread(QRunnable):
    def __init__(self, operation: str, regex_patterns: list = None, folder_path: Path = None, file_patterns: list[str] = None):
        super().__init__()
        self.signals = RegexProcessorSignals()
        self.operation = operation
        self.regex_patterns = regex_patterns if regex_patterns is not None else []
        self.folder_path = folder_path
        self.file_patterns = file_patterns if file_patterns is not None else []
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
            self.signals.finished.emit(results)   # ✅ Always emit, even if empty

    def extract_named_groups_from_regex(self, regex_pattern: str) -> list[str]:
        group_pattern = r'\(\?P<(\w+)>'
        return re.findall(group_pattern, regex_pattern)

    def process_files(self, files: list[Path], compiled_patterns: list, pattern_group_names: list) -> list[dict[str, Any]]:
        total = len(files)
        results = []

        all_group_names = set()
        for group_names in pattern_group_names:
            all_group_names.update(group_names)
            
        use_pattern_prefix = len(all_group_names) < sum(len(gn) for gn in pattern_group_names)

        for index, filepath in enumerate(files, start=1):
            self.signals.program_output_text.emit(f"Processing file: {filepath.name}")
            
            try:
                if not filepath.is_file() or not filepath.exists():
                    self.signals.program_output_text.emit(f"Skipping inaccessible file {filepath.name}")
                    continue

                with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                    line_count = 0
                    for line_number, line in enumerate(f, start=1):
                        line_count += 1
                        line = line.strip()
                        if not line:
                            continue

                        for pattern_idx, (compiled_regex, group_names) in enumerate(zip(compiled_patterns, pattern_group_names), 1):
                            try:
                                for match in compiled_regex.finditer(line):
                                    result = {"File": filepath.name, "Line": line_number}
                                    if group_names:
                                        for group_name, group_value in match.groupdict().items():
                                            col_name = f"Pattern{pattern_idx}_{group_name}" if use_pattern_prefix else group_name
                                            result[col_name] = str(group_value) if group_value is not None else ""
                                    else:
                                        result[f"Pattern{pattern_idx}_Match"] = str(match.group(0)) if match.group(0) is not None else ""
                                    results.append(result)
                            except Exception as match_error:
                                self.signals.program_output_text.emit(f"Regex error on line {line_number} in {filepath.name}: {str(match_error)}")
                                continue

            except Exception as file_error:
                self.signals.program_output_text.emit(f"File error in {filepath.name}: {str(file_error)}")
                continue

            progress = int((index / total) * 100)
            self.signals.progress_update.emit(progress)

        self.signals.program_output_text.emit(f"Processed {total} files in total!")
        return results

    def search_files(self) -> list[dict[str, Any]]:
        if not self.folder_path or not self.folder_path.exists():
            raise ValueError("Invalid or non-existent folder path")
            
        if not self.regex_patterns:
            raise ValueError("No regex patterns provided. Exiting.")
            
        files = []
        if self.file_patterns and any(fp.strip() for fp in self.file_patterns):
            valid_patterns = [fp.strip() for fp in self.file_patterns if fp.strip()]
            for pattern in valid_patterns:
                files.extend(self.folder_path.glob(pattern))
            total = len(files)
            self.signals.program_output_text.emit(f"Found {total} files using patterns: {valid_patterns}")
        else:
            files = list(self.folder_path.glob('*.*'))
            total = len(files)
            self.signals.program_output_text.emit(f"Found {total} files (all files)")
            
        if not files:
            self.signals.program_output_text.emit("No files found to search")
            self.signals.finished.emit([])
            return
            
        compiled_patterns = []
        pattern_group_names = []
        
        for regex in self.regex_patterns:
            try:
                compiled = re.compile(regex)
                group_names = self.extract_named_groups_from_regex(regex)
                if not group_names:
                    self.signals.program_output_text.emit(f"Warning: Pattern '{regex}' has no named groups; using 'Match' as column")
                compiled_patterns.append(compiled)
                pattern_group_names.append(group_names)
            except re.error as e:
                raise ValueError(f"Invalid regex pattern '{regex}': {e}")
        
        self.signals.program_output_text.emit("Starting file processing")
        results = self.process_files(files, compiled_patterns, pattern_group_names)
        self.signals.program_output_text.emit(f"File processing complete, {len(results)} matches found")
        
        return results