import os
import re
import sys
from pathlib import Path

from PySide6.QtCore import QProcess, QSettings, QSortFilterProxyModel, Qt, QThreadPool, QTimer, Slot
from PySide6.QtGui import QAction, QActionGroup, QCloseEvent, QGuiApplication, QPixmap
from PySide6.QtWidgets import QFileDialog, QInputDialog, QMainWindow, QMenu, QMessageBox, QSplitter

from app_paths import APP_ICON_FILE, CONFIG_DIR, CONFIG_FILE, DARK_THEME_FILE, LIGHT_THEME_FILE
from core.models.results_model import ResultsTableModel
from core.patterns.pattern_profiles import PatternProfileService, PatternSpec
from core.patterns.regex_builder import RegexBuilder
from core.search.engine import PatternDef, PatternError, SearchOptions, compile_patterns
from gui.ui.main.LogSearcherUI_ui import Ui_MainWindow
from services.config.config_handler import ConfigHandler
from services.mixins.signal_handlers import SignalHandlerMixin
from services.utils.helpers import HelperMethods
from services.workers.search_worker import SearchWorker
from services.workers.thread_worker import Worker

AUTOFILL_KEY = "custom_regex_autofill"

# Legacy config entries were sometimes saved as "name = expression" strings.
_LEGACY_ENTRY = re.compile(r"^(?P<name>[A-Za-z_]\w*) = (?P<expression>.+)$", re.DOTALL)

EXPORT_FILTER_XLSX = "Excel Workbook (*.xlsx)"
EXPORT_FILTER_CSV = "CSV, comma separated (*.csv)"
EXPORT_FILTER_CSV_SEMI = "CSV, semicolon separated - Excel in EU locales (*.csv)"


# ----------------------------
# Helpers for window state
# ----------------------------

LAYOUT_CLASSIC = "classic"
LAYOUT_MODERN = "modern"
LAYOUT_SETTING = "ui/layout"
MODERN_THEME_FILE = DARK_THEME_FILE.with_name("modern.qss")


def resolve_ui_layout(settings: QSettings) -> str:
    """Command line (--alt-ui / --classic-ui) overrides the saved choice."""
    if "--alt-ui" in sys.argv:
        return LAYOUT_MODERN
    if "--classic-ui" in sys.argv:
        return LAYOUT_CLASSIC
    value = str(settings.value(LAYOUT_SETTING, LAYOUT_CLASSIC))
    return value if value in (LAYOUT_CLASSIC, LAYOUT_MODERN) else LAYOUT_CLASSIC


def save_window_state(window: QMainWindow, settings: QSettings, prefix: str = ""):
    settings.setValue(f"{prefix}geometry", window.saveGeometry())
    settings.setValue(f"{prefix}windowState", window.saveState())
    for splitter in window.findChildren(QSplitter):
        if splitter.objectName():
            settings.setValue(f"{prefix}splitter/{splitter.objectName()}", splitter.saveState())


def restore_window_state(window: QMainWindow, settings: QSettings, prefix: str = ""):
    geometry = settings.value(f"{prefix}geometry")
    if geometry:
        window.restoreGeometry(geometry)
    state = settings.value(f"{prefix}windowState")
    if state:
        window.restoreState(state)
    for splitter in window.findChildren(QSplitter):
        splitter_state = settings.value(f"{prefix}splitter/{splitter.objectName()}") if splitter.objectName() else None
        if splitter_state:
            splitter.restoreState(splitter_state)

    # Clamp the window into the visible screen space (e.g. monitor unplugged).
    screen = window.screen() or QGuiApplication.primaryScreen()
    if screen is None:
        return
    available = screen.availableGeometry()
    win_geom = window.frameGeometry()
    if not available.contains(win_geom):
        window.resize(min(win_geom.width(), available.width()), min(win_geom.height(), available.height()))
        window.move(
            max(available.left(), min(win_geom.left(), available.right() - window.width())),
            max(available.top(), min(win_geom.top(), available.bottom() - window.height())),
        )


class MainWindow(QMainWindow, SignalHandlerMixin):
    def __init__(self):
        super().__init__()

        self.settings = QSettings("Jovan", "MatchaRegex")
        self.ui_layout = resolve_ui_layout(self.settings)
        if self.ui_layout == LAYOUT_MODERN:
            from gui.ui.main.modern_main_window_ui import Ui_ModernMainWindow
            self.ui = Ui_ModernMainWindow()
        else:
            self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # Each layout remembers its own geometry/splitters.
        self._state_prefix = "" if self.ui_layout == LAYOUT_CLASSIC else "modern/"
        restore_window_state(self, self.settings, self._state_prefix)

        # Single shared config handler (the regex manager dialog uses this one too).
        self.config_handler = ConfigHandler(CONFIG_DIR, CONFIG_FILE, main_window=self)
        self.helper = HelperMethods(main_window=self)
        self.regex_builder = RegexBuilder(main_window=self)

        self.regex_patterns: list[PatternSpec] = []
        self._pattern_counter = 0
        self.output_file_path: str = ""
        self.last_export_directory: str = str(self.settings.value("last_export_directory", str(Path.home())))
        self._search_worker: SearchWorker | None = None
        self._export_worker: Worker | None = None
        self._regex_manager = None

        # Theme / icon (attributes are also read by the regex manager dialog)
        self.dark_theme_file = DARK_THEME_FILE
        self.light_theme_file = LIGHT_THEME_FILE
        self.app_icon = QPixmap(str(APP_ICON_FILE))
        self.current_app_theme = self.settings.value("Application_Theme", "dark.qss")

        # Results: model → filter/sort proxy → view
        self.results_model = ResultsTableModel(parent=self)
        self.summary_model = ResultsTableModel(parent=self)
        self.proxy_model = QSortFilterProxyModel(self)
        self.proxy_model.setSourceModel(self.results_model)
        self.proxy_model.setFilterKeyColumn(-1)  # all columns
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        table = self.ui.table_widget_results
        table.setModel(self.proxy_model)
        table.horizontalHeader().setSortIndicator(-1, Qt.SortOrder.AscendingOrder)
        table.setSortingEnabled(True)

        # Debounce timers
        self._filter_timer = QTimer(self, singleShot=True, interval=250)
        self._filter_timer.timeout.connect(self._apply_table_filter)
        self._folder_info_timer = QTimer(self, singleShot=True, interval=400)
        self._folder_info_timer.timeout.connect(
            lambda: self.helper.show_relevant_info(self.ui.line_edit_files_folder.text()))

        self.thread_pool = QThreadPool(self)  # used for exports
        if self.ui_layout == LAYOUT_CLASSIC:
            self.ui.button_search_result_export_to_csv.setText("Export (Excel / CSV)")

        self.setup_application()
        if self.ui_layout == LAYOUT_MODERN:
            self._initialize_theme(MODERN_THEME_FILE)
        else:
            self._initialize_theme(DARK_THEME_FILE if self.current_app_theme == "dark.qss" else LIGHT_THEME_FILE)

    def setup_application(self):
        self.connect_ui_events()
        self.connect_menu_bar_actions()
        self.connect_helper_method_signals(self.helper)
        if hasattr(self.ui.list_widget_regex, "header_edited"):
            self.ui.list_widget_regex.header_edited.connect(self._on_pattern_header_edited)
        self.action_import_pattern_json = QAction("Import Pattern Profile JSON", self)
        self.action_import_pattern_json.triggered.connect(self.on_importPatternProfileJson)
        self._update_autofill_menu()
        self._install_view_menu()
        self.on_checkBoxCheckedLimitRows()
        self._set_visible_of_widgets(False)
        if self.ui_layout == LAYOUT_MODERN:
            self.ui.progress_bar.hide()

        # Empty state + row count badge (only layouts that provide them).
        for signal in (self.proxy_model.rowsInserted, self.proxy_model.rowsRemoved,
                       self.proxy_model.modelReset, self.proxy_model.layoutChanged):
            signal.connect(self._update_results_state)
        self._update_results_state()

    # ======================================================================
    # Layout switching
    # ======================================================================

    def _install_view_menu(self):
        menu = QMenu("&View", self)
        group = QActionGroup(self)
        group.setExclusive(True)
        for layout, label in ((LAYOUT_CLASSIC, "&Classic Layout"), (LAYOUT_MODERN, "&Alternative Layout")):
            action = QAction(label, self, checkable=True)
            action.setChecked(layout == self.ui_layout)
            action.triggered.connect(lambda _checked=False, value=layout: self._switch_layout(value))
            group.addAction(action)
            menu.addAction(action)
        self.ui.menubar.insertMenu(self.ui.menuHelp.menuAction(), menu)
        self.menu_view = menu

    def _switch_layout(self, layout: str):
        if layout == self.ui_layout:
            return
        self.settings.setValue(LAYOUT_SETTING, layout)
        name = "alternative" if layout == LAYOUT_MODERN else "classic"
        reply = QMessageBox.question(
            self, "Switch Layout",
            f"The {name} layout will be used after a restart.\n\nRestart MatchaRegex now?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes,
        )
        if reply == QMessageBox.StandardButton.Yes and self.close():
            args = [a for a in sys.argv if a not in ("--alt-ui", "--classic-ui")]
            if Path(sys.executable).stem.lower().startswith("python"):
                QProcess.startDetached(sys.executable, args)          # running from source
            else:
                QProcess.startDetached(sys.executable, args[1:])      # compiled executable

    @Slot()
    def _update_results_state(self, *_):
        rows = self.proxy_model.rowCount()
        stack = getattr(self.ui, "results_stack", None)
        if stack is not None:
            has_columns = self.proxy_model.columnCount() > 0
            stack.setCurrentWidget(self.ui.table_widget_results if has_columns else self.ui.results_empty_state)
        badge = getattr(self.ui, "label_result_count", None)
        if badge is not None:
            total = self.proxy_model.sourceModel().rowCount() if self.proxy_model.sourceModel() else 0
            badge.setText(f"{rows:,} of {total:,}" if rows != total else f"{total:,} rows")
            badge.setVisible(self.proxy_model.columnCount() > 0)

    # ======================================================================
    # Patterns
    # ======================================================================

    @staticmethod
    def parallel_worker_count() -> int:
        """Half of the logical CPUs, at least 1."""
        return max(1, (os.cpu_count() or 2) // 2)

    def _next_pattern_name(self) -> str:
        existing = {p.name for p in self.regex_patterns}
        while True:
            self._pattern_counter += 1
            name = f"Pattern{self._pattern_counter}"
            if name not in existing:
                return name

    @staticmethod
    def _validate_regex(expression: str) -> str | None:
        try:
            re.compile(expression)
            return None
        except re.error as exc:
            return str(exc)

    def _append_pattern(self, pattern_spec: PatternSpec) -> bool:
        if any(p.name == pattern_spec.name and p.expression == pattern_spec.expression for p in self.regex_patterns):
            return False
        self.regex_patterns.append(pattern_spec)
        pattern_list = self.ui.list_widget_regex
        if hasattr(pattern_list, "add_pattern"):  # alternative layout: Header | Regex columns
            pattern_list.add_pattern(pattern_spec.name, pattern_spec.expression, pattern_spec.header)
        else:
            pattern_list.addItem(f"{pattern_spec.name} = {pattern_spec.expression}")
        return True

    @Slot(int, str)
    def _on_pattern_header_edited(self, row: int, header: str):
        if 0 <= row < len(self.regex_patterns):
            self.regex_patterns[row].header = header
            shown = header or "Match"
            self.ui.statusbar.showMessage(f"Matches of '{self.regex_patterns[row].name}' go to column '{shown}'.", 5000)

    def _pattern_from_entry(self, entry) -> PatternSpec | None:
        """Accepts {"name", "expression"[, "header"]} dicts, plain regex strings and legacy "name = expr" strings."""
        header = ""
        if isinstance(entry, dict):
            expression = str(entry.get("expression", "")).strip()
            name = str(entry.get("name", "")).strip()
            header = str(entry.get("header", "") or "").strip()
        else:
            expression = str(entry).strip()
            name = ""
            legacy = _LEGACY_ENTRY.match(expression)
            if legacy and self._validate_regex(legacy["expression"]) is None:
                name, expression = legacy["name"], legacy["expression"]
        if not expression:
            return None
        return PatternSpec(name=name or self._next_pattern_name(), expression=expression, header=header)

    def _update_autofill_menu(self):
        """Rebuild the Autofill menu from the saved presets."""
        menu = self.ui.menuAutofill
        menu.clear()
        presets = self.config_handler.get(AUTOFILL_KEY, {})
        if isinstance(presets, dict):
            for preset_name, value in presets.items():
                expressions = value.get("regex_expression", []) if isinstance(value, dict) else []
                action = QAction(str(preset_name), self)
                action.triggered.connect(lambda _checked=False, e=expressions: self._set_autofill_regex_expressions(e))
                menu.addAction(action)
        menu.addSeparator()
        menu.addAction(self.action_import_pattern_json)

    def _set_autofill_regex_expressions(self, expressions: list):
        added, invalid = 0, []
        for entry in expressions or []:
            spec = self._pattern_from_entry(entry)
            if spec is None:
                continue
            if self._validate_regex(spec.expression) is not None:
                invalid.append(spec.name)
                continue
            added += self._append_pattern(spec)
        self.ui.statusbar.showMessage(f"Loaded {added} pre-built regex expression(s).", 6000)
        if invalid:
            QMessageBox.warning(self, "Invalid Patterns",
                                "These saved patterns are not valid regular expressions and were skipped:\n"
                                + "\n".join(invalid))

    # ======================================================================
    # Theme / window
    # ======================================================================

    def _initialize_theme(self, theme_file: Path):
        try:
            if Path(theme_file).is_file():
                self.setStyleSheet(Path(theme_file).read_text(encoding="utf-8"))
        except OSError as ex:
            QMessageBox.critical(self, "Theme load error", f"Failed to load theme: {ex}")

    def closeEvent(self, event: QCloseEvent):
        worker = self._search_worker
        if worker is not None and worker.isRunning():
            reply = QMessageBox.question(
                self, "Exit Confirmation",
                "A search is still running. Stop it and exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No,
            )
            if reply != QMessageBox.StandardButton.Yes:
                event.ignore()
                return
            worker.cancel()
            worker.wait(10_000)

        # Let a running export finish writing its file.
        if self.thread_pool.activeThreadCount():
            self.ui.statusbar.showMessage("Waiting for export to finish...")
            self.thread_pool.waitForDone(30_000)

        self.settings.setValue("Application_Theme", self.current_app_theme)
        save_window_state(self, self.settings, self._state_prefix)
        super().closeEvent(event)

    # ======================================================================
    # Menu bar slots
    # ======================================================================

    @Slot()
    def on_openInputDirectory(self):
        self.helper.open_dir_in_file_manager(self.ui.line_edit_files_folder.text().strip())

    @Slot()
    def on_openOutputDirectory(self):
        path = Path(self.output_file_path) if self.output_file_path else None
        self.helper.open_dir_in_file_manager(str(path.parent) if path and path.exists() else "")

    @Slot()
    def on_openPrebuiltRegexManager(self):
        from gui.dialogs.regex_expression_manager import PreBuiltRegexManagerWidget

        if self._regex_manager is None:
            self._regex_manager = PreBuiltRegexManagerWidget(main_window=self)
        self._regex_manager.show()
        self._regex_manager.raise_()
        self._regex_manager.activateWindow()

    @Slot()
    def on_browseFolder(self):
        self.helper.browse_folder_path(line_edit=self.ui.line_edit_files_folder)

    @Slot()
    def on_importPatternProfileJson(self):
        json_path, _ = QFileDialog.getOpenFileName(
            self, "Select Pattern Profile JSON", str(Path.home()), "JSON Files (*.json)")
        if not json_path:
            return
        try:
            service = PatternProfileService(Path(json_path))
            profiles = service.list_profiles()
            selected_profile, accepted = QInputDialog.getItem(
                self, "Select Pattern Profile", "Pattern profile:", profiles, 0, False)
            if not accepted or not selected_profile:
                return

            pattern_specs = service.get_profile_patterns(selected_profile)
            if not pattern_specs:
                QMessageBox.information(self, "Pattern Import", "No regex patterns were found in the selected profile.")
                return

            invalid = [f"{p.name}: {err}" for p in pattern_specs if (err := self._validate_regex(p.expression))]
            if invalid:
                QMessageBox.warning(self, "Pattern Import",
                                    "The profile contains invalid regular expressions:\n\n" + "\n".join(invalid))
                return

            loaded_count = sum(self._append_pattern(spec) for spec in pattern_specs)

            preset_name = f"Imported_{Path(json_path).stem}_{selected_profile}"
            # Key path as list: preset names may contain dots (e.g. "logs.v2").
            self.config_handler.set(
                [AUTOFILL_KEY, preset_name, "regex_expression"],
                [{"name": p.name, "expression": p.expression} for p in pattern_specs],
            )
            self._update_autofill_menu()
            self.ui.statusbar.showMessage(
                f"Imported {loaded_count} regex patterns from profile '{selected_profile}'.", 10000)
        except Exception as ex:
            QMessageBox.critical(self, "Pattern Import Error", f"Failed to import pattern profile: {ex}")

    # ======================================================================
    # Pattern list
    # ======================================================================

    @Slot()
    def on_convertString(self):
        sample = self.ui.line_edit_string_to_regex.text()
        regex = self.regex_builder.build_smart_regex(sample)
        if not regex:
            QMessageBox.information(self, "Input Warning", "Please enter a valid sample string.")
            return
        regex_input = self.ui.line_edit_regex
        if regex_input.text().strip():
            # Append (concatenate) so a pattern can be built piece by piece.
            regex_input.setText(regex_input.text() + regex)
            self.ui.statusbar.showMessage("Appended generated regex to the existing pattern.", 5000)
        else:
            regex_input.setText(regex)
            self.ui.statusbar.showMessage(f"Generated Regex: {regex}", 5000)

    @Slot()
    def add_regexToListWidget(self):
        expression = self.ui.line_edit_regex.text().strip()
        if not expression:
            QMessageBox.information(self, "Missing regex pattern", "Please enter a regex pattern in the input field.")
            return
        if (error := self._validate_regex(expression)) is not None:
            QMessageBox.warning(self, "Invalid Regex", f"The pattern is not a valid regular expression:\n\n{error}")
            return
        if any(p.expression == expression for p in self.regex_patterns):
            QMessageBox.information(self, "Duplicate Regex", "This regex pattern already exists in the active list.")
            return
        self._append_pattern(PatternSpec(name=self._next_pattern_name(), expression=expression))
        self.ui.line_edit_regex.clear()
        self.ui.statusbar.showMessage(f"Added {expression} regex pattern to the list.", 5000)

    @Slot()
    def on_removeSelectedRegexPattern(self):
        row = self.ui.list_widget_regex.currentRow()
        if 0 <= row < len(self.regex_patterns):
            item = self.ui.list_widget_regex.takeItem(row)
            del self.regex_patterns[row]
            self.ui.statusbar.showMessage(f"Removed {item.text()} from list!", 5000)

    @Slot()
    def on_removeAllRegexPattern(self):
        if self.ui.list_widget_regex.count():
            self.ui.list_widget_regex.clear()
            self.regex_patterns.clear()
            self._pattern_counter = 0
            self.ui.statusbar.showMessage("Removed all regex patterns from list!", 5000)

    # ======================================================================
    # Search
    # ======================================================================

    def _set_search_running(self, running: bool):
        btn = self.ui.button_start_search
        btn.setEnabled(True)
        btn.setText("Stop Search" if running else "Start Search")
        if self.ui_layout == LAYOUT_MODERN:
            self.ui.progress_bar.setVisible(running)  # status bar: only while searching
        for widget in (self.ui.button_search_result_clear_results, self.ui.button_count_occurrences,
                       self.ui.button_regex_pattern_remove_all, self.ui.button_regex_pattern_remove_selected):
            widget.setEnabled(not running)
        self.ui.statusbar.showMessage("Searching..." if running else "Ready to search.", 0 if running else 5000)

    @Slot()
    def on_startSearch(self):
        # Button doubles as "Stop Search" while a search runs.
        if self._search_worker is not None:
            self._search_worker.cancel()
            self.ui.button_start_search.setEnabled(False)
            self.ui.button_start_search.setText("Stopping...")
            return

        folder_text = self.ui.line_edit_files_folder.text().strip()
        folder_path = Path(folder_text) if folder_text else None
        if folder_path is None or not folder_path.is_dir():
            QMessageBox.information(self, "Input Warning", "Please specify a valid folder path.")
            return
        if not self.regex_patterns:
            QMessageBox.information(self, "Input Warning", "Please add at least one regex pattern.")
            return

        patterns = tuple(PatternDef(p.name, p.expression, p.header) for p in self.regex_patterns)
        try:
            compile_patterns(patterns)  # fail fast in the GUI with a clear message
        except PatternError as exc:
            QMessageBox.warning(self, "Regex Error", str(exc))
            return

        limit_rows = self.ui.checkbox_limit_rows.isChecked() and self.ui.spinbox_rows.value() > 0
        options = SearchOptions(
            folder=folder_path,
            patterns=patterns,
            file_patterns=tuple(p.strip() for p in self.ui.line_edit_file_pattern.text().split(",") if p.strip()),
            segmentation_mode=self.ui.combobox_segmentation_mode.currentText(),
            whole_file=self.ui.checkbox_multiline_search.isChecked(),
            max_rows=self.ui.spinbox_rows.value() if limit_rows else 0,
        )
        workers = self.parallel_worker_count() if self.ui.checkbox_enable_parallel_processing.isChecked() else 1

        self._clear_results_view()
        self.ui.program_output.clear()
        self.ui.program_output.append(
            f"Starting search ({'parallel, ' + str(workers) + ' processes' if workers > 1 else 'sequential'}, "
            f"{'whole-file' if options.whole_file else options.segmentation_mode + ' segmentation'})...")

        worker = SearchWorker(options, workers=workers, parent=self)
        worker.schema_ready.connect(self._on_search_schema)
        worker.rows_ready.connect(self.results_model.append_rows)
        worker.progress_changed.connect(self.handle_progress_bar)
        worker.log_message.connect(self.handle_program_output)
        worker.search_failed.connect(self.handle_critical_message)
        worker.search_completed.connect(self._on_search_completed)
        worker.finished.connect(self._on_search_thread_finished)  # QThread.finished: run() has returned
        self._search_worker = worker
        self._set_search_running(True)
        worker.start()

    @Slot(list)
    def _on_search_schema(self, columns: list):
        self.proxy_model.setSourceModel(self.results_model)
        self.results_model.reset(columns)

    @Slot(dict)
    def _on_search_completed(self, summary: dict):
        rows = self.results_model.rowCount()
        if summary:
            state = "cancelled" if summary.get("cancelled") else "finished"
            self.ui.program_output.append(
                f"Search {state}: {summary.get('searched_files', 0)}/{summary.get('total_files', 0)} files, "
                f"{rows} matches, {summary.get('failed_files', 0)} unreadable, "
                f"{summary.get('elapsed', 0):.2f}s.")

        if rows:
            self.ui.table_widget_results.resizeColumnsToContents()
            self.ui.combobox_count_occurrences.clear()
            self.ui.combobox_count_occurrences.addItems(self.results_model.columns())
            self._set_visible_of_widgets(True)
        elif summary and not summary.get("cancelled"):
            self.ui.program_output.append(
                "No matches found. Tip: patterns spanning several lines need "
                "'Multiline search' or a matching segmentation mode.")
            QMessageBox.information(self, "Search Complete", "No matches found.")

    @Slot()
    def _on_search_thread_finished(self):
        worker = self._search_worker
        self._search_worker = None
        if worker is not None:
            worker.deleteLater()
        self.handle_progress_bar(0)
        self._set_search_running(False)
        self._set_visible_of_widgets(self.results_model.rowCount() > 0)

    # ======================================================================
    # Results table
    # ======================================================================

    def _clear_results_view(self):
        self.ui.line_edit_filter_table_text.blockSignals(True)
        self.ui.line_edit_filter_table_text.clear()
        self.ui.line_edit_filter_table_text.blockSignals(False)
        self.proxy_model.setFilterFixedString("")
        self.ui.table_widget_results.horizontalHeader().setSortIndicator(-1, Qt.SortOrder.AscendingOrder)
        self.proxy_model.sort(-1)
        self.proxy_model.setSourceModel(self.results_model)
        self.results_model.reset()
        self.summary_model.reset()
        self.ui.combobox_count_occurrences.clear()
        self._set_visible_of_widgets(False)

    @Slot()
    def _apply_table_filter(self):
        self.proxy_model.setFilterFixedString(self.ui.line_edit_filter_table_text.text().strip())

    @Slot()
    def on_clearResults(self):
        self._clear_results_view()
        self.ui.statusbar.showMessage("Cleared results table!", 5000)

    @Slot()
    def on_countOccurrences(self):
        from core.analysis.count_occurrences import count_occurrences_by_key

        if not self.results_model.rowCount():
            QMessageBox.warning(self, "No Data", "No search results available to count.")
            return
        key_field = self.ui.combobox_count_occurrences.currentText()
        if not key_field:
            QMessageBox.information(self, "Input Warning", "Please select a key field to count occurrences.")
            return

        columns, summary = count_occurrences_by_key(self.results_model.rows(), key_field)
        if not summary:
            QMessageBox.information(self, "No Data", f"No values found in column '{key_field}'.")
            return
        self.summary_model.reset(columns, summary)
        self.proxy_model.setSourceModel(self.summary_model)
        self.ui.table_widget_results.resizeColumnsToContents()
        self.ui.statusbar.showMessage(
            f"Showing occurrence counts for '{key_field}'. Start a new search or clear to return.", 8000)

    def _visible_snapshot(self) -> tuple[list[str], list[dict]]:
        """Rows exactly as shown (filtered + sorted), taken on the GUI thread."""
        source: ResultsTableModel = self.proxy_model.sourceModel()
        columns = source.columns()
        proxy = self.proxy_model
        if proxy.rowCount() == source.rowCount() and proxy.sortColumn() < 0:
            return columns, source.rows()
        return columns, [source.row_at(proxy.mapToSource(proxy.index(r, 0)).row()) for r in range(proxy.rowCount())]

    @Slot()
    def on_exportResults(self):
        if self._export_worker is not None:
            QMessageBox.information(self, "Export", "An export is already running.")
            return
        columns, rows = self._visible_snapshot()
        if not rows:
            QMessageBox.information(self, "Export Information", "No results to export.")
            return

        default_dir = self.last_export_directory if Path(self.last_export_directory).is_dir() else str(Path.home())
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self, "Export Result", str(Path(default_dir) / "Regex_Search_Result.xlsx"),
            ";;".join((EXPORT_FILTER_XLSX, EXPORT_FILTER_CSV, EXPORT_FILTER_CSV_SEMI)),
        )
        if not file_path:
            self.ui.statusbar.showMessage("Export cancelled by user.", 5000)
            return

        if selected_filter == EXPORT_FILTER_CSV_SEMI:
            delimiter = ";"
        elif selected_filter == EXPORT_FILTER_CSV or file_path.lower().endswith(".csv"):
            delimiter = ","
        else:
            delimiter = None

        self.output_file_path = file_path
        self.last_export_directory = str(Path(file_path).parent)
        self.settings.setValue("last_export_directory", self.last_export_directory)

        from services.export.exporter import ExportSignals, export_results

        worker = Worker(export_results, file_path, columns, rows, delimiter, signals_factory=ExportSignals)
        worker.signals.status.connect(self.handle_statusbar_message)
        worker.signals.failed.connect(self.handle_critical_message)
        worker.signals.succeeded.connect(self._on_export_succeeded)
        worker.signals.failed.connect(self._on_export_done)
        self._export_worker = worker
        self.ui.button_search_result_export_to_csv.setEnabled(False)
        self.thread_pool.start(worker)

    @Slot(str)
    def _on_export_succeeded(self, path: str):
        self.output_file_path = path
        self._on_export_done()
        self.handle_export_success(path)

    @Slot()
    def _on_export_done(self, *_):
        self._export_worker = None
        self.ui.button_search_result_export_to_csv.setEnabled(True)

    # ======================================================================
    # Misc
    # ======================================================================

    @Slot()
    def on_clearProgramOutput(self):
        if self.ui.program_output.toPlainText():
            self.ui.program_output.clear()
            self.ui.statusbar.showMessage("Output cleared!", 5000)

    @Slot()
    def on_checkBoxCheckedLimitRows(self, *_):
        enabled = self.ui.checkbox_limit_rows.isChecked()
        self.ui.spinbox_rows.setEnabled(enabled)
        if not enabled:
            self.ui.spinbox_rows.setValue(0)

    @Slot()
    def on_parallelProcessingInfo(self):
        QMessageBox.information(
            self, "Parallel Processing Information",
            "Searches always run in a separate worker process, so the window stays responsive "
            "and 'Stop Search' works even if a pattern gets stuck (catastrophic backtracking).\n\n"
            f"With parallel processing enabled, files are searched by {self.parallel_worker_count()} "
            "processes at once (half of your CPU cores). This speeds up searches over many files "
            "but uses more CPU and memory. Results are still returned in file order.",
        )
