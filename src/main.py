# File: main.py 
from modules.signal_handlers import SignalHandlerMixin
from modules.helpers import HelperMethods
from resources.interface.LogSearcherUI_ui import Ui_MainWindow

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
)
from PySide6.QtCore import (
    Slot,
    QThreadPool,
)
import sys
from pathlib import Path

# from resources.interface.qrc import LogSearcher_resource_rc

class MainWindow(QMainWindow, SignalHandlerMixin):
    def __init__(self):
        super().__init__()

        # Create and set up the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        from modules.regex_builder import RegexBuilder
        self.helper = HelperMethods(main_window=self)
        self.regex_builder = RegexBuilder(main_window=self)
        
        self.regex_patterns: list[str] = []
        
        self.init_thread_pool()
        self.setup_application()
        
    def setup_application(self):
        """Initialize the application components"""
        self.connect_ui_events()  # From mixin
        
    def init_thread_pool(self):
        # Initialize the thread pool
        self.thread_pool = QThreadPool()

        # Optional: Set maximum thread count (default is system dependent)
        max_threads = self.thread_pool.maxThreadCount()
        self.thread_pool.setMaxThreadCount(max_threads)
        
    # === App Methods & Logic === #
    

    @Slot()
    def on_filesFolderTextChanged(self):
        input_field = self.ui.line_edit_files_folder
        self.connect_helper_method_signals(self.helper) # Connect signals from helper methods
        self.helper.input_field_text_changed(line_edit=input_field)
        
    # Button event handlers
    @Slot()
    def on_browseFolder(self): # Handler for "Browse Folder" button
        input_field = self.ui.line_edit_files_folder
        self.connect_helper_method_signals(self.helper) # Connect signals from helper methods
        self.helper.browse_folder_path(line_edit=input_field)
    
    @Slot()
    def on_convertString(self): # Handler for "Convert String to Regex" button
        try:
            sample = self.ui.line_edit_string_to_regex.text()
            regex = self.regex_builder.build_smart_regex(sample)
            if regex:
                # Add generated regex to the regex input field
                regex_input = self.ui.line_edit_regex
                if not regex_input.text().strip():
                    regex_input.setText(regex)
                    self.ui.statusbar.showMessage(f"Generated Regex: {regex}", 5000)
                else:
                    regex_input.setText(regex_input.text().strip() + " , " + regex)
                    self.ui.statusbar.showMessage("Added generated regex after existing regex, separated by a comma.", 5000)
            else:
                QMessageBox.warning(self, "Input Error", "Please enter a valid sample string.")
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(ex)}")
            
    @Slot()
    def add_regexToListWidget(self): # Handler for "Add Regex to List" button
        try:
            regex_input = self.ui.line_edit_regex.text().strip()
            text_for_conversion = self.ui.line_edit_string_to_regex.text().strip()
            if regex_input:
                # Add text that is was used for conversion as regex to the header input field
                if self.ui.line_edit_headers.text().strip() == "" and text_for_conversion:
                    self.ui.line_edit_headers.setText(text_for_conversion)
                    self.ui.statusbar.showMessage(f"Added header: {text_for_conversion}", 5000)
                else:
                    self.ui.line_edit_headers.setText(self.ui.line_edit_headers.text().strip() + "," + text_for_conversion)
                # Split by comma and add each regex to the list widget
                regex_list = [r.strip() for r in regex_input.split(",") if r.strip()]
                for regex in regex_list:
                    self.ui.list_widget_regex.addItem(regex)
                    self.regex_patterns.append(regex)
                self.ui.line_edit_regex.clear()
                self.ui.statusbar.showMessage(f"Added {len(regex_list)} regex pattern(s) to the list.", 5000)
            else:
                QMessageBox.warning(self, "Input Error", "Please enter at least one regex pattern.")
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(ex)}")
            
        
    @Slot()
    def on_startSearch(self): # Handler for "Start Search" button
        try:
            # Clear previous output
            self.ui.program_output.clear()
            
            # Validate inputs
            folder_path = Path(self.ui.line_edit_files_folder.text().strip())
            file_patterns = [p.strip() for p in self.ui.line_edit_file_pattern.text().split(",") if p.strip()]
            regex_patterns = self.regex_patterns
            headers = self.ui.line_edit_headers.text().strip().split(",") if self.ui.line_edit_headers.text().strip() else []
            
            if not folder_path.exists() or not folder_path.is_dir():
                QMessageBox.warning(self, "Input Error", "Please specify a valid folder path.")
                return
            if not regex_patterns:
                QMessageBox.warning(self, "Input Error", "Please add at least one regex pattern.")
                return
            if not headers:
                QMessageBox.warning(self, "Input Error", "Please specify at least one header.")
                return
            if len(headers) < len(regex_patterns):
                QMessageBox.warning(self, "Input Error", "Number of headers should be at least equal to the number of regex patterns.")
                return
            
            from modules.helpers import SearcherThread
            self.ui.statusbar.showMessage("Search started...", 5000)
            
            # Create and start the search thread
            search_thread = SearcherThread(
                operation='search_files', 
                main_window=self,
                regex_patterns=regex_patterns,
                headers=headers,
                folder_path=folder_path,
                file_patterns=file_patterns)
            
            self._connect_searcher_thread_signals(search_thread) # Connected signals and slots
            
            self.thread_pool.start(search_thread)
            
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(ex)}")
            
            
if __name__ == "__main__":
    # Initialize the application
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
