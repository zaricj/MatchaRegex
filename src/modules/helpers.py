from resources.interface.LogSearcherUI_ui import Ui_MainWindow
from PySide6.QtWidgets import QFileDialog, QLineEdit
from PySide6.QtCore import QObject, Signal, QRunnable, Slot
import pandas as pd
from pathlib import Path
import re

class HelperMethodSignals(QObject):
    program_output_text = Signal(str)         # Emitted for program output
    statusbar_show_message = Signal(str, int) # Emitted to show message in status bar (message, timeout)

class HelperMethods:
    def __init__(self, main_window=None):
        self.main_window = main_window
        self.ui: Ui_MainWindow = main_window.ui
        self.signals = HelperMethodSignals()
        
    def browse_folder_path(self, line_edit: QLineEdit):
        folder_path = QFileDialog.getExistingDirectory(
            self.main_window,
            "Select Folder",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )
        if folder_path:
            line_edit.setText(folder_path)
            self.show_relevant_info(folder_path=line_edit.text())
    
    def input_field_text_changed(self, line_edit: QLineEdit) -> None:
        """On input field text change, this method gets triggered. It runs the 'show_relevant_info' method

        Args:
            line_edit (QLineEdit): The input field to look for
        """
        self.show_relevant_info(folder_path=line_edit.text())
    
    def show_relevant_info(self, folder_path: str) -> None:
        """Prints out the relevant info based on browse button press or just text changed in the specified input field

        Args:
            folder_path (str): Path of the folder which is grabbed from the QFileDialog window.
        """
        path = Path(folder_path)
        if path.exists() and path.is_dir():
            
            files = []
            file_patterns = self.ui.line_edit_file_pattern.text().strip().split(",")

            # Fixed: Check if file_patterns is not empty and contains valid patterns
            if file_patterns and file_patterns != ['']:
                self.signals.program_output_text.emit(f"Using file patterns: {file_patterns}")

                for pattern in file_patterns:
                    pattern = pattern.strip()
                    if pattern:
                        files.extend(path.glob(pattern))
                        self.signals.program_output_text.emit(f"Pattern '{pattern}' matched {len(list(path.glob(pattern)))} files.")
                if len(files) > 0:
                    self.signals.statusbar_show_message.emit(f"Selected folder: {folder_path} | Total files: {len(files)} | Using patterns: {file_patterns}", 5000)
            else:
                files = list(path.glob('*.*'))
                if len(files) > 0:
                    self.signals.statusbar_show_message.emit(f"Selected folder: {folder_path} | Total files: {len(files)}", 5000)


class SearcherSignals(QObject):
    message_information = Signal(str, str)    # Emitted on Information - QMessageBox (title, message)
    message_warning = Signal(str, str)        # Emitted on Warning - QMessageBox (title, message)
    message_critical = Signal(str, str)       # Emitted on Critical - QMessageBox (title, message)
    program_output_text = Signal(str)         # Emitted for program output
    statusbar_show_message = Signal(str, int) # Emitted to show message in status bar (message, timeout)
    widget_enable = Signal(object, bool)      # Emitted to enable/disable a widget (widget, enable)
    finished = Signal(pd.DataFrame)           # Emitted when the thread is finished

class SearcherThread(QRunnable):
    def __init__(self, operation: str, main_window=None, regex_patterns: list = None, headers: list[str] = None, folder_path: Path = None, file_patterns: list[str] = None):
        """Searcher thread for performing file searches based on regex patterns.

        Args:
            operation (str): Operation type to perform
            main_window: Main window reference
            regex_patterns (list): List of regex patterns to search for
            headers (list[str]): List of headers corresponding to regex patterns
            folder_path (Path): Path to folder containing files to search
            file_patterns (list[str]): List of file patterns to match (e.g., ['*.txt', '*.log'])
        """
        super().__init__()
        self.operation = operation
        # Use empty lists as defaults instead of mutable defaults
        self.regex_patterns = regex_patterns if regex_patterns is not None else []
        self.headers = headers if headers is not None else []
        self.folder_path = folder_path
        self.file_patterns = file_patterns if file_patterns is not None else []
        self.signals = SearcherSignals()
        self.ui: Ui_MainWindow = main_window.ui if main_window else None
        self.setAutoDelete(True)  # Automatically clean up when done

    @Slot()
    def run(self):
        """Routes execution based on the operation."""
        try:
            if self.operation == 'search_files':
                self.search_files()
            else:
                raise ValueError(f"Unknown operation: {self.operation}")
        except Exception as e:
            self.signals.message_critical.emit("Operation Error", str(e))
            
        finally:
            # Always notify the main thread that this runnable is finished
            try:
                # Fixed: Pass empty DataFrame if no results
                if not hasattr(self, '_results_df'):
                    self.signals.finished.emit(pd.DataFrame())
                else:
                    self.signals.finished.emit(self._results_df)
            except Exception as ex:
                self.signals.message_critical.emit("Thread Finish Error", str(ex))
        
    def search_files(self):
        try:
            self.signals.program_output_text.emit("Search started...")
            
            # Fixed: Add null check for UI
            if self.ui:
                self.signals.widget_enable.emit(self.ui.button_start_search, False)
            
            # Validation checks
            if not self.folder_path or not self.folder_path.exists():
                raise ValueError("Invalid or non-existent folder path")
                
            if not self.regex_patterns:
                raise ValueError("No regex patterns provided")
                
            if not self.headers:
                raise ValueError("No headers provided")
                
            if len(self.regex_patterns) != len(self.headers):
                raise ValueError("Number of regex patterns must match number of headers")
            
            # Logic for searching files
            results = []
            files = []
            
            # Fixed: Handle file patterns correctly
            if self.file_patterns and any(fp.strip() for fp in self.file_patterns):
                # Filter out empty patterns
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
                self._results_df = pd.DataFrame()
                return
            
            # Pre-compile regex patterns for better performance
            compiled_patterns = []
            for regex in self.regex_patterns:
                try:
                    compiled_patterns.append(re.compile(regex))
                except re.error as e:
                    raise ValueError(f"Invalid regex pattern '{regex}': {e}")
            
            for index, filepath in enumerate(files, start=1):
                self.signals.program_output_text.emit(f"Processing file {index}/{total}: {filepath.name}")
                
                try:
                    # Fixed: Better file handling with proper error handling
                    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                        line_number = 0
                        for line in f:
                            line_number += 1
                            line = line.strip()
                            if not line:  # Skip empty lines
                                continue
                                
                            # Check each regex pattern against the line
                            for compiled_regex, header in zip(compiled_patterns, self.headers):
                                if compiled_regex.search(line):
                                    # Store result with corresponding header and additional info
                                    result = {
                                        "File": filepath.name,
                                        "Line": line_number,
                                        header: line
                                    }
                                    results.append(result)
                                    self.signals.program_output_text.emit(f"Match found for '{header}' at line {line_number}")
                                    
                except Exception as file_error:
                    self.signals.message_warning.emit(
                        "File Processing Error", 
                        f"Error processing {filepath.name}: {str(file_error)}"
                    )
                    continue
                
                # Update status
                if self.ui:
                    # Fixed: Use proper signal emission for status updates
                    self.signals.program_output_text.emit(f"Processed {index}/{total} files")
            
            # Convert results to DataFrame
            if results:
                self._results_df = pd.DataFrame(results)
                self.signals.program_output_text.emit(f"Total matches found: {len(self._results_df)}")
            else:
                self.signals.program_output_text.emit("No matches found.")
                self._results_df = pd.DataFrame()

            self.signals.program_output_text.emit("Search finished.")
            
        except Exception as e:
            self.signals.message_critical.emit("Search Error", str(e))
            self._results_df = pd.DataFrame()
            
        finally:
            # Re-enable the search button
            if self.ui:
                self.signals.widget_enable.emit(self.ui.button_start_search, True)