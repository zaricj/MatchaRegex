"""Signal wiring and generic slots for :class:`app.MainWindow`."""
import webbrowser
from pathlib import Path
from typing import TYPE_CHECKING

from PySide6.QtCore import QUrl, Slot
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QMessageBox

from services.utils.helpers import HelperMethods

if TYPE_CHECKING:
    from gui.ui.main.LogSearcherUI_ui import Ui_MainWindow


class SignalHandlerMixin:
    """Mixin providing generic slots and the UI signal connections."""

    ui: "Ui_MainWindow"

    # ============= GENERIC SLOTS =============

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
    def handle_export_success(self, file_path: str):
        """Success dialog with 'Open Folder' / 'Open File' buttons."""
        msg_box = QMessageBox(self)
        if not self.app_icon.isNull():
            msg_box.setIconPixmap(self.app_icon)
        msg_box.setWindowTitle("Export Successful")
        msg_box.setText("Result exported successfully!")
        msg_box.setInformativeText(f"File saved to:\n{file_path}")
        open_folder_btn = msg_box.addButton("Open Folder", QMessageBox.ButtonRole.ActionRole)
        open_file_btn = msg_box.addButton("Open File", QMessageBox.ButtonRole.ActionRole)
        ok_btn = msg_box.addButton(QMessageBox.StandardButton.Ok)
        msg_box.setDefaultButton(ok_btn)
        msg_box.exec()

        clicked = msg_box.clickedButton()
        if clicked == open_folder_btn:
            QDesktopServices.openUrl(QUrl.fromLocalFile(str(Path(file_path).parent)))
        elif clicked == open_file_btn:
            QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))

    # ============= WIDGET STATE HELPERS =============

    def _set_visible_of_widgets(self, visibility: bool):
        """Show/hide (classic) or enable/disable (alternative layout) the result tools."""
        widgets = [self.ui.button_count_occurrences, self.ui.combobox_count_occurrences,
                   self.ui.line_edit_filter_table_text, self.ui.label_filter_text]
        if getattr(self.ui, "hide_result_tools_when_empty", True):
            for widget in widgets:
                widget.setVisible(visibility)
        else:
            widgets += [self.ui.button_search_result_export_to_csv, self.ui.button_search_result_clear_results]
            for widget in widgets:
                widget.setEnabled(visibility)

    # ============= CONNECTION METHODS =============

    def connect_helper_method_signals(self, helper: HelperMethods):
        helper.signals.program_output_text.connect(self.handle_program_output)
        helper.signals.statusbar_show_message.connect(self.handle_statusbar_message)

    def connect_menu_bar_actions(self):
        self.ui.actionRegex_101.triggered.connect(lambda: webbrowser.open("https://regex101.com"))
        self.ui.actionRegex_Cheatsheet.triggered.connect(lambda: webbrowser.open("https://regexlearn.com/cheatsheet"))
        self.ui.actionOpen_Input_Folder.triggered.connect(self.on_openInputDirectory)
        self.ui.actionOpen_Output_Folder.triggered.connect(self.on_openOutputDirectory)
        self.ui.actionOpen_Regex_Expression_Manager.triggered.connect(self.on_openPrebuiltRegexManager)

    def connect_ui_events(self):
        """Connect all UI element events to their handlers."""
        ui = self.ui

        # Line edits (debounced: no filesystem / filter work on every keystroke)
        ui.line_edit_files_folder.textChanged.connect(self._folder_info_timer.start)
        ui.line_edit_file_pattern.textChanged.connect(self._folder_info_timer.start)
        ui.line_edit_filter_table_text.textChanged.connect(self._filter_timer.start)
        ui.line_edit_regex.returnPressed.connect(self.add_regexToListWidget)

        # Font size of program output
        ui.combobox_font_size_program_output.currentTextChanged.connect(
            lambda size: ui.program_output.setStyleSheet(f'font: {size} "Consolas";'))

        # Buttons
        ui.button_browse_folder.clicked.connect(self.on_browseFolder)
        ui.button_string_to_regex.clicked.connect(self.on_convertString)
        ui.button_add_regex_to_list_widget.clicked.connect(self.add_regexToListWidget)
        ui.button_start_search.clicked.connect(self.on_startSearch)
        ui.button_regex_pattern_remove_selected.clicked.connect(self.on_removeSelectedRegexPattern)
        ui.button_regex_pattern_remove_all.clicked.connect(self.on_removeAllRegexPattern)
        ui.button_search_result_export_to_csv.clicked.connect(self.on_exportResults)
        ui.button_search_result_clear_results.clicked.connect(self.on_clearResults)
        ui.button_clear_program_output.clicked.connect(self.on_clearProgramOutput)
        ui.button_parallel_processing_info.clicked.connect(self.on_parallelProcessingInfo)
        ui.button_count_occurrences.clicked.connect(self.on_countOccurrences)

        # Checkboxes
        ui.checkbox_limit_rows.toggled.connect(self.on_checkBoxCheckedLimitRows)
