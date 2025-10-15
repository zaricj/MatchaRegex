from typing import Any
import re
from pathlib import Path
from PySide6.QtCore import QObject, Signal, QRunnable, Slot, QMutex, QMutexLocker

# ============================================
# SIGNALS
# ============================================

class RegexProcessorSignals(QObject):
    message_information = Signal(str, str)
    message_warning = Signal(str, str)
    message_critical = Signal(str, str)
    program_output_text = Signal(str)
    statusbar_show_message = Signal(str, int)
    progress_update = Signal(int)
    finished = Signal(list)

class FileProcessorSignals(QObject):
    """Signals for individual file processing tasks"""
    file_processed = Signal(int)  # Emits file index when complete
    results_ready = Signal(list)  # Emits results from this file

# ============================================
# INDIVIDUAL FILE PROCESSOR
# ============================================

class FileProcessorWorker(QRunnable):
    """Worker that processes a single file"""
    
    def __init__(self, filepath: Path, file_index: int, compiled_patterns: list,
                 col_name_maps: list, multiline: bool, max_results: int = 0):
        super().__init__()
        self.filepath = filepath
        self.file_index = file_index
        self.compiled_patterns = compiled_patterns
        self.col_name_maps = col_name_maps
        self.multiline = multiline
        self.max_results = max_results
        self.signals = FileProcessorSignals()
        self.setAutoDelete(True)
    
    @Slot()
    def run(self):
        """Process a single file"""
        results = []
        
        try:
            if not self.filepath.is_file() or not self.filepath.exists():
                self.signals.file_processed.emit(self.file_index)
                self.signals.results_ready.emit(results)
                return
            
            with open(self.filepath, "r", encoding="utf-8", errors="replace", buffering=65536) as f:
                if self.multiline:
                    text = f.read()
                    results = self._process_multiline(text)
                else:
                    results = self._process_line_by_line(f)
                    
        except Exception:
            # Silently handle errors, just emit empty results
            pass
        
        # Emit results and signal completion
        self.signals.file_processed.emit(self.file_index)
        self.signals.results_ready.emit(results)
    
    def _process_multiline(self, text: str) -> list[dict[str, Any]]:
        """Process file content as a single multiline string"""
        results = []
        
        for compiled_regex, (col_map, match_col) in zip(self.compiled_patterns, self.col_name_maps):
            for match in compiled_regex.finditer(text):
                result = {"File": self.filepath.name}
                
                if col_map:
                    groupdict = match.groupdict()
                    for group_name, col_name in col_map.items():
                        result[col_name] = groupdict.get(group_name) or ""
                else:
                    result[match_col] = match.group(0) or ""
                
                results.append(result)
                
                # Check result limit
                if self.max_results > 0 and len(results) >= self.max_results:
                    return results
        
        return results
    
    def _process_line_by_line(self, file_handle) -> list[dict[str, Any]]:
        """Process file line by line"""
        results = []
        
        for line_number, line in enumerate(file_handle, start=1):
            line = line.strip()
            if not line:
                continue
            
            for compiled_regex, (col_map, match_col) in zip(self.compiled_patterns, self.col_name_maps):
                try:
                    for match in compiled_regex.finditer(line):
                        result = {"File": self.filepath.name, "Line": line_number}
                        
                        if col_map:
                            groupdict = match.groupdict()
                            for group_name, col_name in col_map.items():
                                result[col_name] = groupdict.get(group_name) or ""
                        else:
                            result[match_col] = match.group(0) or ""
                        
                        results.append(result)
                        
                        # Check result limit
                        if self.max_results > 0 and len(results) >= self.max_results:
                            return results
                            
                except Exception:
                    continue
        
        return results

# ============================================
# COORDINATOR/MANAGER
# ============================================

class ParallelRegexProcessor(QObject):
    """Coordinator that manages parallel file processing - NOT a QRunnable"""
    
    def __init__(self, thread_pool, regex_patterns: list, folder_path: Path,
                 file_patterns: list[str], multiline: bool = False, max_rows: int = 0):
        super().__init__()
        self.thread_pool = thread_pool
        self.signals = RegexProcessorSignals()
        self.regex_patterns = regex_patterns
        self.folder_path = folder_path
        self.file_patterns = file_patterns
        self.multiline = multiline
        self.max_rows = max_rows
        
        # Thread-safe result collection
        self.all_results = []
        self.results_mutex = QMutex()
        self.files_completed = 0
        self.total_files = 0
        self.files_mutex = QMutex()
        self.result_limit_reached = False
    
    def start(self):
        """Start the parallel processing"""
        try:
            # Gather files
            files = self._gather_files()
            if not files:
                self.signals.program_output_text.emit("No files found to search")
                self.signals.finished.emit([])
                return
            
            self.total_files = len(files)
            
            # Compile patterns
            compiled_patterns, col_name_maps = self._compile_patterns()
            if not compiled_patterns:
                self.signals.finished.emit([])
                return
            
            self.signals.program_output_text.emit(f"Starting parallel processing of {self.total_files} files")
            
            # Create and submit file processors
            for index, filepath in enumerate(files):
                worker = FileProcessorWorker(
                    filepath=filepath,
                    file_index=index,
                    compiled_patterns=compiled_patterns,
                    col_name_maps=col_name_maps,
                    multiline=self.multiline,
                    max_results=self.max_rows
                )
                
                # Connect signals
                worker.signals.file_processed.connect(self._on_file_processed)
                worker.signals.results_ready.connect(self._on_results_ready)
                
                # Submit to thread pool
                self.thread_pool.start(worker)
            
        except Exception as e:
            self.signals.message_critical.emit("Search Error", f"Coordinator error: {str(e)}")
            self.signals.finished.emit([])
    
    @Slot(int)
    def _on_file_processed(self, file_index: int):
        """Called when a file completes processing"""
        with QMutexLocker(self.files_mutex):
            self.files_completed += 1
            progress = int((self.files_completed / self.total_files) * 100)
            self.signals.progress_update.emit(progress)
            
            # Check if all files are done
            if self.files_completed >= self.total_files:
                # All done - emit final results
                with QMutexLocker(self.results_mutex):
                    final_results = self.all_results[:self.max_rows] if self.max_rows > 0 else self.all_results
                    self.signals.program_output_text.emit(
                        f"Processed {self.total_files} files, {len(final_results)} matches found"
                    )
                    self.signals.finished.emit(final_results)
    
    @Slot(list)
    def _on_results_ready(self, results: list):
        """Called when a file returns results"""
        if not results:
            return
        
        with QMutexLocker(self.results_mutex):
            # Check if we've already hit the limit
            if self.result_limit_reached:
                return
            
            # Add results
            if self.max_rows > 0:
                remaining = self.max_rows - len(self.all_results)
                if remaining > 0:
                    self.all_results.extend(results[:remaining])
                    
                    if len(self.all_results) >= self.max_rows:
                        self.result_limit_reached = True
                        self.signals.program_output_text.emit(f"Reached result limit of {self.max_rows}")
            else:
                self.all_results.extend(results)
    
    def _gather_files(self) -> list[Path]:
        """Gather files based on patterns"""
        files = []
        
        if self.file_patterns and any(fp.strip() for fp in self.file_patterns):
            valid_patterns = [fp.strip() for fp in self.file_patterns if fp.strip()]
            file_set = set()
            for pattern in valid_patterns:
                file_set.update(self.folder_path.glob(pattern))
            files = list(file_set)
            self.signals.program_output_text.emit(
                f"Found {len(files)} files using patterns: {valid_patterns}"
            )
        else:
            files = list(self.folder_path.glob('*.*'))
            self.signals.program_output_text.emit(f"Found {len(files)} files (all files)")
        
        return files
    
    def _compile_patterns(self) -> tuple[list, list]:
        """Compile regex patterns and prepare column mappings"""
        compiled_patterns = []
        pattern_group_names = []
        
        flags = re.MULTILINE if self.multiline else 0
        
        for regex in self.regex_patterns:
            try:
                compiled = re.compile(regex, flags)
                group_names = self._extract_named_groups(regex)
                compiled_patterns.append(compiled)
                pattern_group_names.append(group_names)
            except re.error as e:
                self.signals.message_critical.emit(
                    "Regex Error",
                    f"Invalid regex pattern '{regex}': {e}"
                )
                return [], []
        
        # Pre-build column name mappings
        all_group_names = set()
        for group_names in pattern_group_names:
            all_group_names.update(group_names)
        
        use_pattern_prefix = len(all_group_names) < sum(len(gn) for gn in pattern_group_names)
        
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
        
        return compiled_patterns, col_name_maps
    
    def _extract_named_groups(self, regex_pattern: str) -> list[str]:
        """Extract named groups from regex pattern"""
        group_pattern = r'\(\?P<(\w+)>'
        return re.findall(group_pattern, regex_pattern)