# File: main.py 

from resources.interface.LogSearcherUI_ui import Ui_MainWindow
from modules.signal_handlers import SignalHandlerMixin
from modules.helpers import HelperMethods
from resources.interface.LogSearcherUI_ui import Ui_MainWindow

from PySide6.QtGui import QPixmap, QGuiApplication, QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QFileDialog,
)
from PySide6.QtCore import (
    Slot,
    QThreadPool,
    QFile, 
    QTextStream,
    QSettings,
    QIODevice,
)
import sys
from pathlib import Path

from modules.config_handler import ConfigHandler

# Constants
CURRENT_DIR = Path(__file__).parent
GUI_CONFIG_DIRECTORY: Path = CURRENT_DIR / "config"
GUI_CONFIG_FILE_PATH: Path = GUI_CONFIG_DIRECTORY / "config.json"

# ----------------------------
# Helpers for window state
# ----------------------------
def save_window_state(window: QMainWindow, settings: QSettings):
    settings.setValue("geometry", window.saveGeometry())
    settings.setValue("windowState", window.saveState())

def restore_window_state(window: QMainWindow, settings: QSettings):
    geometry = settings.value("geometry")
    if geometry:
        window.restoreGeometry(geometry)
    state = settings.value("windowState")
    if state:
        window.restoreState(state)

    # Clamp window into current screen space
    screen = QGuiApplication.primaryScreen()
    available = screen.availableGeometry()
    win_geom = window.frameGeometry()

    if not available.contains(win_geom, proper=False):
        window.resize(
            min(win_geom.width(), available.width()),
            min(win_geom.height(), available.height())
        )
        window.move(
            max(available.left(), min(win_geom.left(), available.right() - window.width())),
            max(available.top(), min(win_geom.top(), available.bottom() - window.height()))
        )

class MainWindow(QMainWindow, SignalHandlerMixin):
    def __init__(self):
        super().__init__()
    
        # Create and set up the UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Setup settings
        self.settings = QSettings("Jovan", "MatchaRegex")
        
        # Restore geometry safely
        restore_window_state(self, self.settings)
        
        from modules.regex_builder import RegexBuilder
        self.helper = HelperMethods(main_window=self)
        self.connect_helper_method_signals(self.helper)
        self.regex_builder = RegexBuilder(main_window=self)
        
        self._active_worker = None
        self.regex_patterns: list[str] = []
        self.output_file_path: str = ""
        
        self.config_handler = ConfigHandler(
            main_window=self,
            config_directory=GUI_CONFIG_DIRECTORY,
            config_file_name=GUI_CONFIG_FILE_PATH,
        )
        
        # Current working dir
        cwd = Path(__file__).parent
        
        # Theme files dark & light
        self.dark_theme_file = cwd / "resources" / "themes" / "dark.qss"
        self.light_theme_file = cwd / "resources" / "themes" / "light.qss"
        
        # GUI Window Icon
        app_icon_path = cwd / "resources" / "interface" / "qrc" / "images" / "matcha-latte.png"
        self.app_icon = QPixmap(app_icon_path.__str__())

        # Current app theme, saved to QSettings
        self.current_app_theme = self.settings.value("Application_Theme", "dark.qss")
        theme_path = self.dark_theme_file if self.current_app_theme == "dark.qss" else self.light_theme_file

        self.init_thread_pool()
        self.setup_application()
        self._initialize_theme(theme_path)
        
    def setup_application(self):
        """Initialize the application components"""
        self.connect_ui_events()  # From mixin (src/modules/signal_handlers.py)
        self.connect_menu_bar_actions() # Menubar actions events connector
        self._update_autofill_menu()
        
    def init_thread_pool(self):
        # Initialize the thread pool
        self.thread_pool = QThreadPool()

        # Optional: Set maximum thread count (default is system dependent)
        max_threads = self.thread_pool.maxThreadCount()
        print(f"Max threads: {max_threads}")
        self.thread_pool.setMaxThreadCount(max_threads)
        
    def _update_autofill_menu(self):
        """Update the autofill menu with custom pre-built xpaths and csv headers"""
        self.ui.menuAutofill.clear()

        custom_autofill = self.config_handler.get("custom_regex_autofill", {})
        for key, value in custom_autofill.items():
            action = QAction(key, self)
            action.triggered.connect(
                lambda checked, v=value: self._set_autofill_regex_expressions(
                    v.get("xpath_expression", []),
                    v.get("csv_header", [])
                )
            )
            self.ui.menuAutofill.addAction(action)
            
    def _set_autofill_regex_expressions(self, expressions: list[str]):
        """Adds the values for regex expressions list widget.

        Args:
            expressions (list[str]): List of regex expressions in the config
        """
        for xpath in expressions:
            if xpath not in self.regex_patterns:
                self.ui.list_widget_regex.addItem(xpath)
                self.regex_patterns.append(xpath)
        
    def closeEvent(self, event):
        self.settings.setValue("Application_Theme", self.current_app_theme)
        save_window_state(self, self.settings)
        super().closeEvent(event)
        
    def _initialize_theme(self, theme_file: str):
        """Initialized UI theme files (.qss)

        Args:
            theme_file (str): File path to the .qss theme file
        """
        try:
            file = QFile(theme_file)
            if not file.open(
                QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text
            ):
                return
            else:
                stream = QTextStream(file)
                stylesheet = stream.readAll()
                self.setStyleSheet(stylesheet)
            file.close()
        except Exception as ex:
            QMessageBox.critical(
                self, "Theme load error", f"Failed to load theme: {str(ex)}"
            )
    
    # === Menu bar slots === #
    # TODO for slots on_openOutputDirectory and on_openInputDirectory, need to perform a check, when directory = "", it opens the root folder of the main.py.
    
    @Slot()
    def on_openInputDirectory(self):
        directory: str = self.ui.line_edit_files_folder.text()
        self.helper.open_dir_in_file_manager(directory)

    @Slot()
    def on_openOutputDirectory(self):
        directory: str = self.output_file_path
        self.helper.open_dir_in_file_manager(directory)
    
    # === App Methods & Logic === #
    
    # ===== Menubar events =====
    
    @Slot() # Opens Pre-built XPaths Manager QWidget
    def on_openPrebuiltXPathsManager(self):
        from widgets.modules.regex_expression_manager import AutofillRegexExpressionsWidget
        self.w = AutofillRegexExpressionsWidget(main_window=self)
        self.w.show()
    
    @Slot()
    def on_filesFolderTextChanged(self):
        input_field = self.ui.line_edit_files_folder
        self.helper.input_field_text_changed(line_edit=input_field)
        
    # Button event handlers
    @Slot()
    def on_browseFolder(self): # Handler for "Browse Folder" button
        input_field = self.ui.line_edit_files_folder
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
                QMessageBox.information(self, "Input Warning", "Please enter a valid sample string.")
        except Exception as ex:
            QMessageBox.critical(self, "Convert String Error", f"An error occurred in string conversion: {str(ex)}")
            
    @Slot()
    def add_regexToListWidget(self): # Handler for "Add Regex to List" button
        try:
            regex_input = self.ui.line_edit_regex.text().strip()
            if regex_input:
                self.ui.list_widget_regex.addItem(regex_input)
                self.regex_patterns.append(regex_input)
                self.ui.line_edit_regex.clear()
                self.ui.statusbar.showMessage(f"Added {regex_input} regex pattern to the list.", 5000)
            else:
                QMessageBox.information(self, "Input Warning", "Please enter a regex pattern first in the input field.")
        except Exception as ex:
            QMessageBox.critical(self, "Add to List Error", f"An error occurred while trying to add regex pattern to list: {str(ex)}")
    
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
        current_items = self.ui.list_widget_regex.count()
        if current_items > 0:
            self.ui.list_widget_regex.clear()
            self.regex_patterns.clear()
            self.ui.statusbar.showMessage("Removed all regex patterns from list!", 5000)
        
    @Slot()
    def on_startSearch(self): # Handler for "Start Search" button
        """Main business logic of app, searches the found files with the set regex patterns"""
        try:
            # Clear previous output
            self.ui.program_output.clear()
            
            # Validate inputs
            folder_path = Path(self.ui.line_edit_files_folder.text().strip())
            file_patterns = [p.strip() for p in self.ui.line_edit_file_pattern.text().split(",") if p.strip()]
            regex_patterns = self.regex_patterns
            multiline_search = self.ui.checkbox_multiline_search.isChecked()
            
            if not folder_path.exists() or not folder_path.is_dir():
                QMessageBox.information(self, "Input Warning", "Please specify a valid folder path.")
                return
            if not regex_patterns:
                QMessageBox.information(self, "Input Warning", "Please add at least one regex pattern.")
                return

            # Disable the button to prevent multiple searches at once
            self.ui.button_start_search.setEnabled(False)
            
            from modules.regex_processor import RegexProcessorThread
            
            # Create and start the search thread
            regex_processor_thread = RegexProcessorThread(
                operation='search_files', 
                regex_patterns=regex_patterns,
                folder_path=folder_path,
                file_patterns=file_patterns,
                multiline=multiline_search)
            
            self._active_worker = regex_processor_thread
            
            self.ui.program_output.append("Starting thread")
            self.connect_regex_processor_signals(regex_processor_thread) # Connected signals and slots
            self.thread_pool.start(regex_processor_thread)
            
        except Exception as ex:
            QMessageBox.critical(self, "Search Error", f"An error occurred in search: {str(ex)}")
    
    @Slot()
    def on_clearResults(self): # Handler for clear table widget
        if self.ui.table_widget_results.columnCount() > 0:
            self.ui.table_widget_results.clearContents()
            self.ui.statusbar.showMessage("Cleared results table!", 5000)

    @Slot()
    def on_exportToExcel(self):
        """Export table_widget_results to Excel file."""
        table = self.ui.table_widget_results
        row_count = table.rowCount()
        col_count = table.columnCount()
        
        if row_count == 0 or col_count == 0:
            QMessageBox.information(self, "Export Information", "No results to export.")
            return
        
        self.output_file_path, _ = QFileDialog.getSaveFileName(
            self, 
            "Export Result", 
            "Regex_Search_Result", 
            "Excel Files (*.xlsx)"
        )
        if self.output_file_path:
            # Get headers
            headers = [table.horizontalHeaderItem(col).text() for col in range(col_count)]

            # Get data
            data = []
            for row in range(row_count):
                row_data = []
                for col in range(col_count):
                    item = table.item(row, col)
                    row_data.append(item.text() if item else "")
                data.append(row_data)

            from modules.excel_exporter import ExcelExporterThread

            excel_exporter_thread = ExcelExporterThread(data, headers, self.output_file_path, self.app_icon)
            self.connect_excel_exporter_signals(excel_exporter_thread)
            self.thread_pool.start(excel_exporter_thread)
        else:
            self.ui.statusbar.showMessage("Action cancelled by user!", 5000)
    
    @Slot()
    def onClearProgramOutput(self):
        """Clear Program Output Textbox"""
        if len(self.ui.program_output.toPlainText()) > 0:
            self.ui.program_output.clear()
            self.ui.statusbar.showMessage("Output cleared!", 5000)
            
if __name__ == "__main__":
    from resources.interface.LogSearcherUI_ui import Ui_MainWindow
    # Initialize the application
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
