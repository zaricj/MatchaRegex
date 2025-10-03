# =====================================================
# APPROACH 1: Mixin Pattern (Recommended)
# =====================================================
# File: modules/signal_handlers.py
import webbrowser
from PySide6.QtGui import QDesktopServices, QPixmap
from PySide6.QtCore import Slot, QUrl
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem
from modules.excel_exporter import ExcelExporterThread
from modules.helpers import HelperMethods
from modules.regex_processor import RegexProcessorThread
import pandas as pd
from pathlib import Path
from resources.interface.LogSearcherUI_ui import Ui_MainWindow

class SignalHandlerMixin:
    """Mixin class to handle all signal connections and slot methods"""
    ui: Ui_MainWindow
    
    def __init__(self):
        super().__init__()
        self._current_excel_exporter = None  # Track current exporter
    
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
    
    @Slot(str, int)
    def handle_statusbar_message(self, message: str, timeout: int = 5000):
        self.ui.statusbar.showMessage(message, timeout)

    @Slot(str)
    def handle_open_url(self, url: str):
        """Handle opening URL (for opening folder)"""
        QDesktopServices.openUrl(QUrl.fromLocalFile(url))

    # ====== START FINISHED SIGNAL SLOTS START====== #
    
    @Slot(list) # For the RegexProcessorThread
    def handle_finished_regex_processor(self, results: list):
        try:
            if results:
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
                self.ui.program_output.append(f"DataFrame created with {len(results_df)} rows, columns:\n{list(results_df.columns)}")
                self.ui.table_widget_results.clear()
                self._populate_results_table(results_df)
            else:
                self.ui.program_output.append("Search completed, but no matches were found.")
                QMessageBox.information(self, "Search Complete", "No matches found.")
        except Exception as e:
            self.ui.program_output.append(f"Error in handle_finished: {str(e)}")
            QMessageBox.critical(self, "Table Error", f"Failed to update results table: {str(e)}")

        self._enable_start_button(True)
        self.handle_progress_bar(0)
        
        # Release worker reference
        if hasattr(self, "_active_worker"):
            self._active_worker = None
    
    @Slot(str, object)
    def handler_excel_exporter_export_success(self, file_path: str, app_icon: QPixmap):
        """Enhanced success handler with 'Open Folder' button"""
        msg_box = QMessageBox()
        msg_box.setIconPixmap(app_icon)
        msg_box.setWindowIcon(app_icon)
        msg_box.setWindowTitle("Export Successful")
        msg_box.setText("Result exported successfully!")
        msg_box.setInformativeText(f"File saved to:\n{file_path}")
        
        # Add custom buttons
        open_folder_btn = msg_box.addButton("Open Folder", QMessageBox.ButtonRole.ActionRole)
        open_file_btn = msg_box.addButton("Open File", QMessageBox.ButtonRole.ActionRole)
        ok_btn = msg_box.addButton(QMessageBox.StandardButton.Ok)
        
        # Set OK as default
        msg_box.setDefaultButton(ok_btn)
        
        # Execute dialog and handle response
        msg_box.exec()
        
        clicked_button = msg_box.clickedButton()
        if clicked_button == open_folder_btn:
            # Open the folder containing the file
            folder_path = str(Path(file_path).parent)
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder_path))
        elif clicked_button == open_file_btn:
            # Open the file directly
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
        
        # Clear the current exporter reference
        self._current_excel_exporter = None
    
    # ====== END FINISHED SIGNAL SLOTS END ====== #
    
    # Method to handle widget enabled states
    def _enable_start_button(self, enable: bool):
        """Helper method to enable or disable the search button."""
        self.ui.button_start_search.setEnabled(enable)
        if enable:
            self.ui.statusbar.showMessage("Ready to search.", 5000)
        else:
            self.ui.statusbar.showMessage("Searching...", 0)
    
    
    # ============= CONNECTION METHODS =============
    
    def connect_regex_processor_signals(self, regex_processor: RegexProcessorThread):
        """Connect the signals from the regex processor thread to the main window's slots."""
        regex_processor.signals.progress_update.connect(self.handle_progress_bar)
        regex_processor.signals.program_output_text.connect(self.handle_program_output)
        regex_processor.signals.statusbar_show_message.connect(self.handle_statusbar_message)
        regex_processor.signals.message_information.connect(self.handle_info_message)
        regex_processor.signals.message_warning.connect(self.handle_warning_message)
        regex_processor.signals.message_critical.connect(self.handle_critical_message)
        regex_processor.signals.finished.connect(self.handle_finished_regex_processor)
        
    def connect_excel_exporter_signals(self, excel_exporter: ExcelExporterThread):
        """Connect the signals from the excel exporter thread to the main window's slots

        Args:
            excel_exporter (ExcelExporterThread): The excel exporter thread instance
        """
        # Store reference to current exporter
        self._current_excel_exporter = excel_exporter
        
        excel_exporter.signals.message_information.connect(self.handle_info_message)
        excel_exporter.signals.message_warning.connect(self.handle_warning_message)
        excel_exporter.signals.message_critical.connect(self.handle_critical_message)
        excel_exporter.signals.statusbar_show_message.connect(self.handle_statusbar_message)
        excel_exporter.signals.export_success_with_path.connect(self.handler_excel_exporter_export_success)
        
    def connect_helper_method_signals(self, helper: HelperMethods):
        """Connect all signals from HelperMethods to appropriate slots"""
        helper.signals.program_output_text.connect(self.handle_program_output)
        helper.signals.statusbar_show_message.connect(self.handle_statusbar_message)
    
    def connect_menu_bar_actions(self):
        self.ui.actionRegex_101.triggered.connect(lambda: webbrowser.open("https://regex101.com"))
        
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
        self.ui.button_search_result_export_to_csv.clicked.connect(self.on_exportToExcel)
        # Clear results click event
        self.ui.button_search_result_clear_results.clicked.connect(self.on_clearResults)
        # Clear program output click event
        self.ui.button_clear_program_output.clicked.connect(self.onClearProgramOutput)
        
        # ====== MENU BAR EVENTS ======
        
        self.ui.actionOpen_Regex_Expression_Manager.triggered.connect(self.on_openPrebuiltXPathsManager)
    
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