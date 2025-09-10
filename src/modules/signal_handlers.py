# =====================================================
# APPROACH 1: Mixin Pattern (Recommended)
# =====================================================
# File: modules/signal_handlers.py
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QMessageBox, QTableWidgetItem
from modules.helpers import SearcherThread, HelperMethods
from resources.interface.LogSearcherUI_ui import Ui_MainWindow
import pandas as pd

class SignalHandlerMixin:
    """Mixin class to handle all signal connections and slot methods"""
    ui: Ui_MainWindow
    
    # ============= SLOT METHODS =============
    
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
        
    @Slot(object, bool)
    def handle_widget_enable(self, widget, enable: bool):
        widget.setEnabled(enable)
        
    @Slot(pd.DataFrame)
    def handle_search_finished(self, results: pd.DataFrame):
        self.ui.statusbar.showMessage("Search finished.", 5000)
        self._populate_results_table(results)
    
    @Slot(str, int)
    def handle_statusbar_message(self, message: str, timeout: int = 5000):
        self.ui.statusbar.showMessage(message, timeout)
    
    # ============= CONNECTION METHODS =============
    
    def connect_searcher_thread_signals(self, worker: SearcherThread):
        """Connect all signals from SearcherThread to appropriate slots"""
        worker.signals.message_information.connect(self.handle_info_message)
        worker.signals.message_warning.connect(self.handle_warning_message)
        worker.signals.message_critical.connect(self.handle_critical_message)
        worker.signals.program_output_text.connect(self.handle_program_output)
        worker.signals.widget_enable.connect(self.handle_widget_enable)
        worker.signals.finished.connect(self.handle_search_finished)
        worker.signals.statusbar_show_message.connect(self.handle_statusbar_message)
        
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
                self.ui.table_widget_results.setItem(row, col, QTableWidgetItem(str(value)))