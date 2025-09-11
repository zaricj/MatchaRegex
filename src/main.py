# File: main.py 
from modules.signal_handlers import SignalHandlerMixin
from modules.helpers import HelperMethods
from resources.interface.LogSearcherUI_ui import Ui_MainWindow

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QFileDialog
)
from PySide6.QtCore import (
    Slot,
    QThreadPool,
)
import sys
from pathlib import Path
import pandas as pd

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
        self.connect_ui_events()  # From mixin (src/modules/signal_handlers.py)
        
    def init_thread_pool(self):
        # Initialize the thread pool
        self.thread_pool = QThreadPool()

        # Optional: Set maximum thread count (default is system dependent)
        max_threads = self.thread_pool.maxThreadCount()
        print(f"Max threads: {max_threads}")
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
            # regex = self.regex_builder.build_smart_regex(sample, group_name="ip", use_groups=True)
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
            if regex_input:
                import re
                group_names = re.findall(r'\(\?P<(\w+)>', regex_input)
                self.ui.list_widget_regex.addItem(regex_input)
                self.regex_patterns.append(regex_input)
                self.ui.line_edit_regex.clear()
                self.ui.statusbar.showMessage(f"Added {regex_input} regex pattern to the list.", 5000)
            else:
                QMessageBox.warning(self, "Input Error", "Please enter at least one regex pattern.")
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(ex)}")
    
    @Slot()
    def on_removeSelectedRegexPattern(self): # Handler for "Remove Selected" button
        """Remove selected pattern from the list."""
        current_row = self.ui.list_widget_regex.currentRow()
        if current_row >= 0:
            self.ui.statusbar.showMessage(f"Removed {self.ui.list_widget_regex.currentItem().text()} from list!", 5000)
            self.ui.list_widget_regex.takeItem(current_row)
            del self.regex_patterns[current_row]
            
    @Slot()
    def on_removeAllRegexPattern(self): # Handler for "Remove All" button
        """Clear all patterns from the list."""
        self.ui.list_widget_regex.clear()
        self.regex_patterns.clear()
        self.ui.statusbar.showMessage("Removed all regex patterns from list!", 5000)
        
    @Slot()
    def on_startSearch(self): # Handler for "Start Search" button
        try:
            # Clear previous output
            self.ui.program_output.clear()
            
            # Validate inputs
            folder_path = Path(self.ui.line_edit_files_folder.text().strip())
            file_patterns = [p.strip() for p in self.ui.line_edit_file_pattern.text().split(",") if p.strip()]
            regex_patterns = self.regex_patterns
            
            if not folder_path.exists() or not folder_path.is_dir():
                QMessageBox.warning(self, "Input Error", "Please specify a valid folder path.")
                return
            if not regex_patterns:
                QMessageBox.warning(self, "Input Error", "Please add at least one regex pattern.")
                return

            # Disable the button to prevent multiple searches at once
            #self.ui.button_start_search.setEnabled(False)
            
            from modules.regex_processor import RegexProcessorThread
            
            # Create and start the search thread
            regex_processor_thread = RegexProcessorThread(
                operation='search_files', 
                regex_patterns=regex_patterns,
                folder_path=folder_path,
                file_patterns=file_patterns)
            
            self.ui.program_output.append("Starting thread")
            self.connect_regex_processor_signals(regex_processor_thread) # Connected signals and slots
            self.thread_pool.start(regex_processor_thread)
            
        except Exception as ex:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(ex)}")
    
    def on_clearResults(self): # Handler for clear table widget
        if self.ui.table_widget_results.columnCount() > 0:
            self.ui.table_widget_results.clear()
            self.results_df = pd.DataFrame() # Clear the DataFrame as well
            self.ui.statusbar.showMessage("Cleared results table!", 5000)
            
    def on_exportToCsv(self):
        if self.results_df.empty:
            QMessageBox.information(self, "Export Failed", "No results to export.")
            return

        # Prompt user for a save location
        file_path, _ = QFileDialog.getSaveFileName(self, "Export Results", "Regex_Search_Result", "CSV Files (*.csv)")
        
        if file_path:
            try:
                self.results_df.to_csv(file_path, index=False)
                QMessageBox.information(self, "Export Successful", f"Results exported to:\n{file_path}")
                self.ui.statusbar.showMessage("Results exported to CSV.", 5000)
            except Exception as e:
                QMessageBox.critical(self, "Export Error", f"Failed to export results: {e}")
            
if __name__ == "__main__":
    # Initialize the application
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
