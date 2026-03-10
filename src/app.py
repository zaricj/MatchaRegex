from gui.ui.main.LogSearcherUI_ui import Ui_MainWindow
from gui.mixins.signal_handlers import SignalHandlerMixin
from gui.utils.helpers import HelperMethods
from services.config.config_handler import ConfigHandler
from PySide6.QtGui import QPixmap, QGuiApplication, QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QFileDialog,
    QInputDialog,
)
from PySide6.QtCore import (
    Slot,
    QThreadPool,
    QFile,
    QTextStream,
    QSettings,
    QIODevice,
    Qt
)
import sys
from pathlib import Path
from core.patterns.pattern_profiles import PatternProfileService, PatternSpec
from services.workers.thread_worker import Worker


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
            max(available.left(), min(win_geom.left(),
                available.right() - window.width())),
            max(available.top(), min(win_geom.top(),
                available.bottom() - window.height()))
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

        from core.patterns.regex_builder import RegexBuilder
        self.helper = HelperMethods(main_window=self)
        self.regex_builder = RegexBuilder(main_window=self)

        self._active_worker = None
        self.regex_patterns: list[PatternSpec] = []
        self.output_file_path: str = ""
        self.current_results: list[dict[str, str]] = []
        # Remember last export directory
        self.last_export_directory: str = self.settings.value(
            "last_export_directory", str(Path.home()))

        self.config_handler = ConfigHandler(
            main_window=self,
            config_directory=GUI_CONFIG_DIRECTORY,
            config_file_name=GUI_CONFIG_FILE_PATH,
        )

        # Current working dir
        cwd = Path(__file__).parent

        # Theme files dark & light
        self.dark_theme_file = cwd / "gui" / "assets" / "styles" / "dark.qss"
        self.light_theme_file = cwd / "gui" / "assets" / "styles" / "light.qss"

        # GUI Window Icon
        app_icon_path = cwd / "gui" / "assets" / "images" / "matcha-latte.png"
        self.app_icon = QPixmap(app_icon_path.__str__())

        # Current app theme, saved to QSettings
        self.current_app_theme = self.settings.value(
            "Application_Theme", "dark.qss")
        theme_path = self.dark_theme_file if self.current_app_theme == "dark.qss" else self.light_theme_file

        self.init_thread_pool()
        self.setup_application()
        self._initialize_theme(theme_path)

    def setup_application(self):
        """Initialize the application components"""
        self.connect_ui_events()  # From mixin (src/modules/signal_handlers.py)
        self.connect_menu_bar_actions()  # Menubar actions events connector
        self._install_dynamic_menu_actions()
        self._update_autofill_menu()
        self.connect_helper_method_signals(self.helper)
        # Hide count occurrences widgets initially
        self._set_visible_of_widgets(False)

    def _install_dynamic_menu_actions(self):
        self.action_import_pattern_json = QAction(
            "Import Pattern Profile JSON", self
        )
        self.action_import_pattern_json.triggered.connect(
            self.on_importPatternProfileJson
        )
        self.ui.menuAutofill.addSeparator()
        self.ui.menuAutofill.addAction(self.action_import_pattern_json)

    def init_thread_pool(self):
        # Initialize the thread pool
        self.thread_pool = QThreadPool()
        thread_perf = self.thread_pool_calculated(performance=1)
        # Optional: Set maximum thread count (default is system dependent)
        self.thread_pool.setMaxThreadCount(
            thread_perf)  # 0 = low, 1 = medium, 2 = high
        self.ui.statusbar.showMessage(
            f"Thread Pool with {thread_perf} threads initialized.", 10000)

    def thread_pool_calculated(self, performance: int = 1) -> int:
        """Returns the calculated thread count based on the system's CPU cores.
        - Low = 1/4 of max threads.
        - Medium = half of max threads.
        - High = Uses all available threads.

        Args:
            performance (int): Performance level (0 = low, 1 = medium, 2 = high). Default is 1 (medium).

        Returns:
            int: Performance-based thread count. 
        """
        max_threads = self.thread_pool.maxThreadCount()
        if performance == 2:  # High performance
            return max_threads

        if performance == 1:  # Medium performance
            return max_threads // 2

        if performance == 0:  # Low performance
            return max_threads // 4

    def _update_autofill_menu(self):
        """Update the autofill menu with custom pre-built xpaths and csv headers"""
        self.ui.menuAutofill.clear()

        custom_autofill = self.config_handler.get("custom_regex_autofill", {})
        for key, value in custom_autofill.items():
            action = QAction(key, self)
            action.triggered.connect(
                lambda checked, v=value: self._set_autofill_regex_expressions(
                    v.get("regex_expression", [])
                )
            )
            self.ui.menuAutofill.addAction(action)
        if hasattr(self, "action_import_pattern_json"):
            self.ui.menuAutofill.addSeparator()
            self.ui.menuAutofill.addAction(self.action_import_pattern_json)

    def _format_pattern_label(self, pattern_name: str, expression: str) -> str:
        return f"{pattern_name} = {expression}"

    def _append_pattern(self, pattern_spec: PatternSpec):
        if any(
            existing.name == pattern_spec.name
            and existing.expression == pattern_spec.expression
            for existing in self.regex_patterns
        ):
            return False

        self.regex_patterns.append(pattern_spec)
        self.ui.list_widget_regex.addItem(
            self._format_pattern_label(pattern_spec.name, pattern_spec.expression)
        )
        return True

    def _set_autofill_regex_expressions(self, expressions: list):
        """Adds the values for regex expressions list widget.

        Args:
            expressions (list[str]): List of regex expressions in the config
        """
        for index, entry in enumerate(expressions, start=1):
            if isinstance(entry, dict):
                pattern_spec = PatternSpec(
                    name=str(entry.get("name", f"Pattern{index}")).strip() or f"Pattern{index}",
                    expression=str(entry.get("expression", "")).strip(),
                )
            else:
                expression = str(entry).strip()
                if not expression:
                    continue
                pattern_spec = PatternSpec(
                    name=f"Pattern{len(self.regex_patterns) + 1}",
                    expression=expression,
                )

            if pattern_spec.expression:
                self._append_pattern(pattern_spec)
        self.ui.statusbar.showMessage(
            "Loaded pre-built regex expressions!", 6000)

    def _save_app_settings(self):
        """Saves app settings to QSettings"""
        self.settings.setValue("Application_Theme", self.current_app_theme)
        save_window_state(self, self.settings)

    def closeEvent(self, event):
        self._save_app_settings()
        if self._active_worker and self._active_worker.isRunning():
            reply = QMessageBox.question(
                self,
                "Exit Confirmation",
                "A task is still running. Are you sure you want to exit?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.No:
                event.ignore()
                return
            else:
                self._active_worker.stop()  # Assuming the worker has a stop method

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
        file_path: Path = Path(self.output_file_path)
        directory: str = file_path.parent.__str__() if file_path.exists() else ""
        self.helper.open_dir_in_file_manager(directory)

    # === App Methods & Logic === #

    # ===== Menubar events =====

    @Slot()  # Opens Pre-built XPaths Manager QWidget
    def on_openPrebuiltXPathsManager(self):
        from gui.dialogs.regex_expression_manager import PreBuiltRegexManagerWidget
        self.w = PreBuiltRegexManagerWidget(main_window=self)
        self.w.show()

    @Slot()
    def on_filesFolderTextChanged(self):
        input_field = self.ui.line_edit_files_folder
        self.helper.input_field_text_changed(line_edit=input_field)

    # Button event handlers
    @Slot()
    def on_browseFolder(self):  # Handler for "Browse Folder" button
        input_field = self.ui.line_edit_files_folder
        self.helper.browse_folder_path(line_edit=input_field)

    @Slot()
    def on_importPatternProfileJson(self):
        json_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Pattern Profile JSON",
            str(Path.home()),
            "JSON Files (*.json)"
        )
        if not json_path:
            return

        try:
            service = PatternProfileService(Path(json_path))
            profiles = service.list_profiles()
            selected_profile, accepted = QInputDialog.getItem(
                self,
                "Select Pattern Profile",
                "Pattern profile:",
                profiles,
                0,
                False,
            )
            if not accepted or not selected_profile:
                return

            pattern_specs = service.get_profile_patterns(selected_profile)
            if not pattern_specs:
                QMessageBox.information(
                    self,
                    "Pattern Import",
                    "No regex patterns were found in the selected profile.",
                )
                return

            loaded_count = 0
            for pattern_spec in pattern_specs:
                if self._append_pattern(pattern_spec):
                    loaded_count += 1

            preset_name = f"Imported_{Path(json_path).stem}_{selected_profile}"
            self.config_handler.set(
                f"custom_regex_autofill.{preset_name}.regex_expression",
                [
                    {"name": pattern.name, "expression": pattern.expression}
                    for pattern in pattern_specs
                ],
            )
            self._update_autofill_menu()
            self.ui.statusbar.showMessage(
                f"Imported {loaded_count} regex patterns from profile '{selected_profile}'.",
                10000,
            )
        except Exception as ex:
            QMessageBox.critical(
                self,
                "Pattern Import Error",
                f"Failed to import pattern profile: {str(ex)}",
            )

    @Slot()
    def on_convertString(self):  # Handler for "Convert String to Regex" button
        try:
            sample = self.ui.line_edit_string_to_regex.text()
            regex = self.regex_builder.build_smart_regex(sample)
            # regex = self.regex_builder.build_smart_regex(sample, group_name="ip", use_groups=True)
            if regex:
                # Add generated regex to the regex input field
                regex_input = self.ui.line_edit_regex
                if not regex_input.text().strip():
                    regex_input.setText(regex)
                    self.ui.statusbar.showMessage(
                        f"Generated Regex: {regex}", 5000)
                else:
                    regex_input.setText(
                        regex_input.text().strip() + " , " + regex)
                    self.ui.statusbar.showMessage(
                        "Added generated regex after existing regex, separated by a comma.", 5000)
            else:
                QMessageBox.information(
                    self, "Input Warning", "Please enter a valid sample string.")
        except Exception as ex:
            QMessageBox.critical(self, "Convert String Error",
                                 f"An error occurred in string conversion: {str(ex)}")

    @Slot()
    def add_regexToListWidget(self):  # Handler for "Add Regex to List" button
        try:
            regex_input = self.ui.line_edit_regex.text().strip()
            if regex_input:
                pattern_spec = PatternSpec(
                    name=f"Pattern{len(self.regex_patterns) + 1}",
                    expression=regex_input,
                )
                if not self._append_pattern(pattern_spec):
                    QMessageBox.information(
                        self,
                        "Duplicate Regex",
                        "This regex pattern already exists in the active list.",
                    )
                    return
                self.ui.line_edit_regex.clear()
                self.ui.statusbar.showMessage(
                    f"Added {regex_input} regex pattern to the list.", 5000)
            else:
                QMessageBox.information(
                    self, "Input Warning", "Please enter a regex pattern first in the input field.")
        except Exception as ex:
            QMessageBox.critical(
                self, "Add to List Error", f"An error occurred while trying to add regex pattern to list: {str(ex)}")

    @Slot()
    # Handler for "Remove Selected" button
    def on_removeSelectedRegexPattern(self):
        """Remove selected pattern from the list."""
        current_row = self.ui.list_widget_regex.currentRow()
        if current_row >= 0:
            self.ui.statusbar.showMessage(
                f"Removed {self.ui.list_widget_regex.currentItem().text()} from list!", 5000)
            self.ui.list_widget_regex.takeItem(current_row)
            del self.regex_patterns[current_row]

    @Slot()
    def on_removeAllRegexPattern(self):  # Handler for "Remove All" button
        """Clear all patterns from the list."""
        current_items = self.ui.list_widget_regex.count()
        if current_items > 0:
            self.ui.list_widget_regex.clear()
            self.regex_patterns.clear()
            self.ui.statusbar.showMessage(
                "Removed all regex patterns from list!", 5000)

    @Slot()
    def on_startSearch(self):  # Handler for "Start Search" button
        """Main business logic of app, searches the found files with the set regex patterns"""
        try:
            # Clear previous output
            self.ui.program_output.clear()

            # Validate inputs
            folder_path = Path(self.ui.line_edit_files_folder.text().strip())
            file_patterns = [
                p.strip() for p in self.ui.line_edit_file_pattern.text().split(",") if p.strip()]
            regex_patterns = self.regex_patterns
            multiline_search = self.ui.checkbox_multiline_search.isChecked()

            if not folder_path.exists() or not folder_path.is_dir():
                QMessageBox.information(
                    self, "Input Warning", "Please specify a valid folder path.")
                return
            if not regex_patterns:
                QMessageBox.information(
                    self, "Input Warning", "Please add at least one regex pattern.")
                return

            # Disable the button to prevent multiple searches at once
            self.ui.button_start_search.setEnabled(False)

            if self.ui.checkbox_enable_parallel_processing.isChecked():

                # Parallel processing version (multi-threaded):
                from core.search.parallel_regex_processor import ParallelRegexProcessor

                # Create and start the search thread
                parallel_processor = ParallelRegexProcessor(
                    thread_pool=self.thread_pool,
                    regex_patterns=regex_patterns,
                    folder_path=folder_path,
                    file_patterns=file_patterns,
                    multiline=multiline_search,
                    max_rows=self.ui.spinbox_rows.value() if self.ui.spinbox_rows.value(
                    ) > 0 and self.ui.checkbox_limit_rows.isChecked() else 0
                )

                self._active_worker = parallel_processor

                self.ui.program_output.append(
                    "Starting parallel worker threads...")
                self.connect_regex_processor_signals(
                    parallel_processor)  # Connected signals and slots

                parallel_processor.run()

            else:
                # Non-parallel processing version (single-threaded):
                from core.search.regex_processor import RegexProcessorSignals, run_regex_search

                # Create and start the search thread non parallel version
                regex_processor_thread = Worker(
                    run_regex_search,
                    regex_patterns=regex_patterns,
                    folder_path=folder_path,
                    file_patterns=file_patterns,
                    multiline=multiline_search,
                    max_rows=self.ui.spinbox_rows.value() if self.ui.spinbox_rows.value(
                    ) > 0 and self.ui.checkbox_limit_rows.isChecked() else 0,
                    signals_factory=RegexProcessorSignals,
                )

                self._active_worker = regex_processor_thread

                self.ui.program_output.append("Starting worker thread...")
                self.connect_regex_processor_signals(
                    regex_processor_thread)  # Connected signals and slots

                self.thread_pool.start(regex_processor_thread)

        except Exception as ex:
            QMessageBox.critical(self, "Search Error",
                                 f"An error occurred in search: {str(ex)}")

    @Slot()
    def on_clearResults(self):  # Handler for clear table widget
        self.ui.table_widget_results.setModel(None)
        self.ui.statusbar.showMessage("Cleared results table!", 5000)
        self.current_results.clear()  # Clear the current results list
        # Hide specified widgets on initial load
        self._set_visible_of_widgets(False)

    @Slot()
    def on_exportToExcel(self):
        """Export table_widget_results to Excel file."""
        table = self.ui.table_widget_results
        model = table.model()
        if model is None:
            return

        row_count = model.rowCount()
        col_count = model.columnCount()

        if row_count == 0 or col_count == 0:
            QMessageBox.information(
                self, "Export Information", "No results to export.")
            return

        # Use last export directory, fall back to home if it doesn't exist
        default_dir = self.last_export_directory if Path(
            self.last_export_directory).exists() else str(Path.home())
        default_file = str(Path(default_dir) / "Regex_Search_Result.xlsx")

        self.output_file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Result",
            default_file,
            "Excel Files (*.xlsx)"
        )
        if self.output_file_path:
            # Save the directory for next time
            self.last_export_directory = str(
                Path(self.output_file_path).parent)
            self.settings.setValue(
                "last_export_directory", self.last_export_directory)

            from services.export.excel_exporter import ExcelExporterSignals, export_table_to_excel

            excel_exporter_thread = Worker(
                export_table_to_excel,
                table,
                row_count,
                col_count,
                self.output_file_path,
                self.app_icon,
                signals_factory=ExcelExporterSignals,
            )
            self.connect_excel_exporter_signals(excel_exporter_thread)
            self.thread_pool.start(excel_exporter_thread)
        else:
            self.ui.statusbar.showMessage("Action cancelled by user!", 5000)

    @Slot()
    def on_clearProgramOutput(self):
        """Clear Program Output Textbox"""
        if len(self.ui.program_output.toPlainText()) > 0:
            self.ui.program_output.clear()
            self.ui.statusbar.showMessage("Output cleared!", 5000)

    @Slot()
    def on_checkBoxCheckedLimitRows(self):
        """Enable/Disable the max rows input field based on the checkbox state."""
        if self.ui.checkbox_limit_rows.isChecked():
            self.ui.spinbox_rows.setEnabled(True)
        else:
            self.ui.spinbox_rows.setEnabled(False)
            self.ui.spinbox_rows.setValue(0)  # Reset to default value

    @Slot()
    def on_parallelProcessingInfo(self):
        """Show information about parallel processing."""
        info_text = (
            "Parallel Processing Info:\n\n"
            "When enabled, the application will utilize multiple threads to process files concurrently. "
            "This can significantly speed up the search process, especially when dealing with large datasets or multiple files.\n\n"
            "However, please note that enabling parallel processing may increase CPU and memory usage. "
            "Ensure that your system has sufficient resources to handle the additional load.\n\n"
            "If you encounter any issues or performance degradation, consider disabling this option."
        )
        QMessageBox.information(
            self, "Parallel Processing Information", info_text)

    @Slot()
    def on_countOccurrences(self):
        from core.analysis.count_occurrences import count_occurrences_by_key

        if not self.current_results:
            QMessageBox.warning(
                self, "No Data", "No search results available to count.")
            return

        key_field = self.ui.combobox_count_occurrences.currentText()

        if not key_field:
            QMessageBox.information(
                self, "Input Warning", "Please select a key field to count occurrences.")
            return

        summary = count_occurrences_by_key(self.current_results, key_field)

        if not summary:
            QMessageBox.information(
                self, "No Data", "No occurrences found for the specified key.")
            return

        # Display the new summary of the count occurrences in the results table
        import pandas as pd
        summary_df = pd.DataFrame(summary, dtype=str)
        self._populate_results_table(summary_df)
