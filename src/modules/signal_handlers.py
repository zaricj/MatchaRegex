# =====================================================
# APPROACH 1: Mixin Pattern (Recommended)
# =====================================================
# File: modules/signal_handlers.py
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem
from modules.helpers import HelperMethods
from modules.regex_processor import RegexProcessorThread
from resources.interface.LogSearcherUI_ui import Ui_MainWindow
import pandas as pd

class SignalHandlerMixin:
    """Mixin class to handle all signal connections and slot methods"""
    ui: Ui_MainWindow
    
    # ============= SLOT METHODS =============
    
    @Slot(int)
    def handle_progress_bar(self, value: int):
        self.ui.progress_bar.setValue(value)
    
    @Slot(str, str)
    def handle_info_message(self, title: str, message: str):
        QMessageBox.information(self, title, message)
        
    @Slot(str, str)
    def handle_warning_message(self, title: str, message: str):
        QMessageBox.warning(self, title, message)
        
    @Slot(str, str)
    def handle_critical_message(self, title: str, message: str):
        QMessageBox.critical(self, title, message)
        
    @Slot(str)
    def handle_program_output(self, text: str):
        self.ui.program_output.append(text)

    @Slot(list)
    def handle_finished(self, results: list):
        self.ui.program_output.append("Received finished signal")
        try:
            if results:
                self.ui.program_output.append(f"Creating DataFrame from {len(results)} matches")
                # Normalize results to ensure consistent keys
                all_keys = set()
                for result in results:
                    all_keys.update(result.keys())
                for result in results:
                    for key in all_keys:
                        if key not in result:
                            result[key] = ""
                # Create DataFrame in main thread
                results_df = pd.DataFrame(results, dtype=str)
                self.ui.program_output.append(f"DataFrame created with {len(results_df)} rows, columns: {list(results_df.columns)}")
                self.ui.table_widget_results.clear()
                self._populate_results_table(results_df)
                self.ui.program_output.append(f"Table updated with {len(results_df)} matches")
            else:
                self.ui.program_output.append("Search completed, but no matches were found.")
                QMessageBox.information(self, "Search Complete", "No matches found.")
        except Exception as e:
            self.ui.program_output.append(f"Error in handle_finished: {str(e)}")
            QMessageBox.critical(self, "Table Error", f"Failed to update results table: {str(e)}")

        self._enable_start_button(True)
        self.handle_progress_bar(0)
    
    def _enable_start_button(self, enable: bool):
        """Helper method to enable or disable the search button."""
        self.ui.button_start_search.setEnabled(enable)
        if enable:
            self.ui.statusbar.showMessage("Ready to search.", 5000)
        else:
            self.ui.statusbar.showMessage("Searching...", 0)
    
    @Slot(str, int)
    def handle_statusbar_message(self, message: str, timeout: int = 5000):
        self.ui.statusbar.showMessage(message, timeout)
    
    # ============= CONNECTION METHODS =============
    
    def connect_regex_processor_signals(self, regex_processor: RegexProcessorThread):
        """Connect the signals from the regex processor thread to the main window's slots."""
        regex_processor.signals.progress_update.connect(self.handle_progress_bar)
        regex_processor.signals.program_output_text.connect(self.handle_program_output)
        regex_processor.signals.statusbar_show_message.connect(self.handle_statusbar_message)
        regex_processor.signals.message_information.connect(self.handle_info_message)
        regex_processor.signals.message_warning.connect(self.handle_warning_message)
        regex_processor.signals.message_critical.connect(self.handle_critical_message)
        regex_processor.signals.finished.connect(self.handle_finished)
        self.ui.program_output.append("Connected regex processor signals")
        
    def connect_helper_method_signals(self, helper: HelperMethods):
        """Connect all signals from HelperMethods to appropriate slots"""
        helper.signals.program_output_text.connect(self.handle_program_output)
        helper.signals.statusbar_show_message.connect(self.handle_statusbar_message)
        
        
    def connect_ui_events(self):
        """Connect all UI element events to their handlers"""
        
        # ====== LINE EDIT EVENTS ======
        
        # Input text changed
        self.ui.line_edit_files_folder.textChanged.connect(self.on_filesFolderTextChanged)
        
        # ====== COMBOBOX EVENTS ======
        
        # Font size for program output item changed
        self.ui.combobox_font_size_program_output.currentTextChanged.connect(lambda: self.ui.program_output.setStyleSheet(f'font: {self.ui.combobox_font_size_program_output.currentText()} "Consolas";'))
        
        # ====== BUTTON EVENTS ====== 
        
        # Browse folder button click event
        self.ui.button_browse_folder.clicked.connect(self.on_browseFolder)
        # Convert string to regex button click event
        self.ui.button_string_to_regex.clicked.connect(self.on_convertString)
        # Add regex button click event
        self.ui.button_add_regex_to_list_widget.clicked.connect(self.add_regexToListWidget)
        # Search button click event
        self.ui.button_start_search.clicked.connect(self.on_startSearch)
        # Removed selected click event (for regex patterns added to QListWidget)
        self.ui.button_regex_pattern_remove_selected.clicked.connect(self.on_removeSelectedRegexPattern)
        # Removed all click event (for regex patterns added to QListWidget)
        self.ui.button_regex_pattern_remove_all.clicked.connect(self.on_removeAllRegexPattern)
        # Export to CSV click event
        self.ui.button_search_result_export_to_csv.clicked.connect(self.on_exportToCsv)
        # Clear results click event
        self.ui.button_search_result_clear_results.clicked.connect(self.on_clearResults)
    
    # ============= HELPER METHODS =============
    
    def _populate_results_table(self, results: pd.DataFrame):
        """Populate the results table with DataFrame data"""
        self.ui.table_widget_results.clear()
        
        if results.empty:
            return
            
        self.ui.table_widget_results.setRowCount(len(results))
        self.ui.table_widget_results.setColumnCount(len(results.columns))
        self.ui.table_widget_results.setHorizontalHeaderLabels(results.columns.tolist())
        
        for row, record in results.iterrows():
            for col, (key, value) in enumerate(record.items()):
                item = QTableWidgetItem(str(value))
                self.ui.table_widget_results.setItem(row, col, item)
