"""
Alternative ("modern") main window layout, built in code.

It exposes exactly the same widget attribute names as the Qt Designer
generated ``Ui_MainWindow`` (LogSearcherUI_ui.py), so ``app.MainWindow`` and
all its logic work unchanged with either layout.

Layout:
    ┌ Source bar ─ Folder [.......][Browse]  Files [.......]   [▶ Start Search] ┐
    ├ Sidebar ──────────────┬ Results ─────────────────────────────────────────┤
    │ Patterns              │ Filter [...]      Count [col▾][Count] [Export][⌫] │
    │  sample [...][Conv.]  │ ┌ table / empty-state ───────────────────────────┐│
    │  regex [....][Add]    │ │                                                ││
    │  ┌Header│Regex ┐     │ └────────────────────────────────────────────────┘│
    │  [Remove] [Clear]     ├ Output ────────────────────── size [10pt▾][Clear] ┤
    │ Search options        │  log ...                                          │
    └───────────────────────┴───────────────────────────────────────────────────┘
    Status bar: messages                                         [progress bar]
"""
from __future__ import annotations

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QAction, QIcon, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMenu,
    QMenuBar,
    QProgressBar,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QSplitter,
    QStackedWidget,
    QStatusBar,
    QTableView,
    QTextEdit,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from gui.assets.qrc import LogSearcher_resource_rc  # noqa: F401  (registers :/images)
from gui.ui.main.pattern_list_widget import PatternListWidget

SEGMENTATION_MODES = ("Auto", "Timestamp", "Exception", "Line")
FONT_SIZES = ("10pt", "11pt", "12pt", "13pt", "14pt", "15pt", "16pt")


def _icon(resource: str | None = None, theme: QIcon.ThemeIcon | None = None) -> QIcon:
    if theme is not None:
        icon = QIcon.fromTheme(theme)
        if not icon.isNull():
            return icon
    return QIcon(resource) if resource else QIcon()


def _card(parent: QWidget, object_name: str) -> tuple[QFrame, QVBoxLayout]:
    frame = QFrame(parent)
    frame.setObjectName(object_name)
    frame.setProperty("card", True)
    layout = QVBoxLayout(frame)
    layout.setContentsMargins(14, 12, 14, 14)
    layout.setSpacing(8)
    return frame, layout


def _title(text: str, parent: QWidget) -> QLabel:
    label = QLabel(text, parent)
    label.setProperty("role", "title")
    return label


def _hint(text: str, parent: QWidget) -> QLabel:
    label = QLabel(text, parent)
    label.setProperty("role", "hint")
    label.setWordWrap(True)
    return label


def _button(text: str, parent: QWidget, variant: str | None = None, icon: QIcon | None = None,
            tooltip: str = "") -> QPushButton:
    button = QPushButton(text, parent)
    if variant:
        button.setProperty("variant", variant)
    if icon is not None and not icon.isNull():
        button.setIcon(icon)
        button.setIconSize(QSize(16, 16))
    if tooltip:
        button.setToolTip(tooltip)
    button.setCursor(Qt.CursorShape.PointingHandCursor)
    return button


class Ui_ModernMainWindow:
    """Drop-in alternative for ``Ui_MainWindow`` (same public attribute names)."""

    # Read by MainWindow: keep result tools visible (disabled) instead of hiding them.
    hide_result_tools_when_empty = False
    layout_name = "modern"

    def setupUi(self, MainWindow: QMainWindow) -> None:
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("MatchaRegex")
        MainWindow.setWindowIcon(QIcon(":/images/matcha-latte.png"))
        MainWindow.setMinimumSize(980, 640)
        MainWindow.resize(1400, 860)  # default; saved geometry is restored afterwards

        self._build_actions(MainWindow)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        root = QVBoxLayout(self.centralwidget)
        root.setContentsMargins(12, 12, 12, 8)
        root.setSpacing(10)

        root.addWidget(self._build_source_bar(self.centralwidget))

        self.main_splitter = QSplitter(Qt.Orientation.Horizontal, self.centralwidget)
        self.main_splitter.setObjectName("main_splitter")
        self.main_splitter.setChildrenCollapsible(False)
        self.main_splitter.setHandleWidth(8)
        self.main_splitter.addWidget(self._build_sidebar(self.main_splitter))

        self.content_splitter = QSplitter(Qt.Orientation.Vertical, self.main_splitter)
        self.content_splitter.setObjectName("content_splitter")
        self.content_splitter.setChildrenCollapsible(False)
        self.content_splitter.setHandleWidth(8)
        self.content_splitter.addWidget(self._build_results_card(self.content_splitter))
        self.content_splitter.addWidget(self._build_output_card(self.content_splitter))
        self.content_splitter.setStretchFactor(0, 4)
        self.content_splitter.setStretchFactor(1, 1)
        self.content_splitter.setSizes([620, 170])

        self.main_splitter.addWidget(self.content_splitter)
        self.main_splitter.setStretchFactor(0, 0)
        self.main_splitter.setStretchFactor(1, 1)
        self.main_splitter.setSizes([360, 1040])
        root.addWidget(self.main_splitter, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self._build_menus(MainWindow)
        self._build_statusbar(MainWindow)
        self._build_shortcuts(MainWindow)
        self._set_tab_order(MainWindow)

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _build_source_bar(self, parent: QWidget) -> QFrame:
        self.source_card, outer = _card(parent, "source_card")
        outer.setContentsMargins(14, 10, 14, 10)
        row = QHBoxLayout()
        row.setSpacing(10)

        self.label_files_folder = QLabel("&Folder", self.source_card)
        self.line_edit_files_folder = QLineEdit(self.source_card)
        self.line_edit_files_folder.setObjectName("line_edit_files_folder")
        self.line_edit_files_folder.setPlaceholderText("Folder containing the log files…")
        self.line_edit_files_folder.setClearButtonEnabled(True)
        self.label_files_folder.setBuddy(self.line_edit_files_folder)

        self.button_browse_folder = _button(
            "Browse…", self.source_card, icon=_icon(theme=QIcon.ThemeIcon.FolderOpen),
            tooltip="Choose the folder to search (Ctrl+O)")
        self.button_browse_folder.setObjectName("button_browse_folder")

        self.label_file_pattern = QLabel("F&iles", self.source_card)
        self.line_edit_file_pattern = QLineEdit(self.source_card)
        self.line_edit_file_pattern.setObjectName("line_edit_file_pattern")
        self.line_edit_file_pattern.setPlaceholderText("*.log, *.txt, **/*.log  (empty = all files)")
        self.line_edit_file_pattern.setToolTip(
            "Comma-separated glob patterns relative to the folder.\n"
            "Use **/ to include sub folders, e.g. **/*.log")
        self.line_edit_file_pattern.setClearButtonEnabled(True)
        self.label_file_pattern.setBuddy(self.line_edit_file_pattern)

        self.button_start_search = _button(
            "Start Search", self.source_card, variant="primary",
            icon=QIcon(":/images/search-file.png"),
            tooltip="Start the search with the current settings (F5 / Ctrl+Enter).\n"
                    "Click again while running to stop.")
        self.button_start_search.setObjectName("button_start_search")
        self.button_start_search.setMinimumWidth(150)
        self.button_start_search.setMinimumHeight(34)

        row.addWidget(self.label_files_folder)
        row.addWidget(self.line_edit_files_folder, 3)
        row.addWidget(self.button_browse_folder)
        row.addSpacing(8)
        row.addWidget(self.label_file_pattern)
        row.addWidget(self.line_edit_file_pattern, 2)
        row.addSpacing(8)
        row.addWidget(self.button_start_search)
        outer.addLayout(row)
        return self.source_card

    def _build_sidebar(self, parent: QWidget) -> QWidget:
        sidebar = QWidget(parent)
        sidebar.setObjectName("sidebar")
        sidebar.setMinimumWidth(300)
        sidebar.setMaximumWidth(560)
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # --- Patterns card ---
        self.patterns_card, pl = _card(sidebar, "patterns_card")
        pl.addWidget(_title("Search patterns", self.patterns_card))

        self.label_string_to_regex = QLabel("Build from &sample text", self.patterns_card)
        self.label_string_to_regex.setProperty("role", "field")
        pl.addWidget(self.label_string_to_regex)
        sample_row = QHBoxLayout()
        self.line_edit_string_to_regex = QLineEdit(self.patterns_card)
        self.line_edit_string_to_regex.setObjectName("line_edit_string_to_regex")
        self.line_edit_string_to_regex.setPlaceholderText("e.g. 192.168.0.1 or 2024-01-31")
        self.label_string_to_regex.setBuddy(self.line_edit_string_to_regex)
        self.button_string_to_regex = _button(
            "Convert", self.patterns_card, icon=QIcon(":/images/convert.png"),
            tooltip="Generate a regex from the sample and put it into the Regex field")
        self.button_string_to_regex.setObjectName("button_string_to_regex")
        sample_row.addWidget(self.line_edit_string_to_regex, 1)
        sample_row.addWidget(self.button_string_to_regex)
        pl.addLayout(sample_row)

        self.label_regex = QLabel("&Regex", self.patterns_card)
        self.label_regex.setProperty("role", "field")
        pl.addWidget(self.label_regex)
        regex_row = QHBoxLayout()
        self.line_edit_regex = QLineEdit(self.patterns_card)
        self.line_edit_regex.setObjectName("line_edit_regex")
        self.line_edit_regex.setProperty("mono", True)
        self.line_edit_regex.setPlaceholderText(r"e.g. user=(?P<user>\w+)")
        self.line_edit_regex.setToolTip("Named groups (?P<name>…) become table columns. Press Enter to add.")
        self.label_regex.setBuddy(self.line_edit_regex)
        self.button_add_regex_to_list_widget = _button(
            "Add", self.patterns_card, variant="accent", icon=_icon(theme=QIcon.ThemeIcon.ListAdd),
            tooltip="Add the pattern to the active list (Enter)")
        self.button_add_regex_to_list_widget.setObjectName("button_add_regex_to_list_widget")
        regex_row.addWidget(self.line_edit_regex, 1)
        regex_row.addWidget(self.button_add_regex_to_list_widget)
        pl.addLayout(regex_row)

        list_header = QHBoxLayout()
        self.label_active_patterns = QLabel("Active", self.patterns_card)
        self.label_active_patterns.setProperty("role", "field")
        list_header.addWidget(self.label_active_patterns)
        list_header.addStretch(1)
        self.button_regex_pattern_remove_selected = _button(
            "Remove", self.patterns_card, variant="ghost", icon=QIcon(":/images/remove-selected.png"),
            tooltip="Remove the selected pattern (Del)")
        self.button_regex_pattern_remove_selected.setObjectName("button_regex_pattern_remove_selected")
        self.button_regex_pattern_remove_all = _button(
            "Clear", self.patterns_card, variant="ghost-danger", icon=QIcon(":/images/remove-all.png"),
            tooltip="Remove all patterns")
        self.button_regex_pattern_remove_all.setObjectName("button_regex_pattern_remove_all")
        list_header.addWidget(self.button_regex_pattern_remove_selected)
        list_header.addWidget(self.button_regex_pattern_remove_all)
        pl.addLayout(list_header)

        self.list_widget_regex = PatternListWidget(self.patterns_card)
        self.list_widget_regex.setObjectName("list_widget_regex")
        self.list_widget_regex.setMinimumHeight(140)
        self.list_widget_regex.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        pl.addWidget(self.list_widget_regex, 1)
        self.label_pattern_list_hint = _hint(
            "Named groups (?P<name>…) become columns automatically. "
            "Double-click a header to rename it.", self.patterns_card)
        pl.addWidget(self.label_pattern_list_hint)
        layout.addWidget(self.patterns_card, 1)

        # --- Options card ---
        self.options_card, ol = _card(sidebar, "options_card")
        ol.addWidget(_title("Search options", self.options_card))
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        form.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)
        form.setHorizontalSpacing(12)
        form.setVerticalSpacing(8)

        self.label_segmentation_mode = QLabel("Se&gmentation", self.options_card)
        self.combobox_segmentation_mode = QComboBox(self.options_card)
        self.combobox_segmentation_mode.setObjectName("combobox_segmentation_mode")
        self.combobox_segmentation_mode.addItems(SEGMENTATION_MODES)
        self.combobox_segmentation_mode.setToolTip(
            "Which text a pattern sees at once:\n"
            "Line – every line on its own\n"
            "Timestamp – log entries starting with HH:MM:SS\n"
            "Exception – exception header with its stack trace\n"
            "Auto – detected from the first 100 lines")
        self.label_segmentation_mode.setBuddy(self.combobox_segmentation_mode)
        form.addRow(self.label_segmentation_mode, self.combobox_segmentation_mode)

        self.checkbox_multiline_search = QCheckBox("Whole-file search (multiline)", self.options_card)
        self.checkbox_multiline_search.setObjectName("checkbox_multiline_search")
        self.checkbox_multiline_search.setToolTip(
            "Patterns may span any number of lines. Overrides segmentation.\n"
            "Files over 256 MB are still searched in segments.")
        form.addRow(self.checkbox_multiline_search)

        parallel_row = QHBoxLayout()
        parallel_row.setSpacing(4)
        self.checkbox_enable_parallel_processing = QCheckBox("Parallel processing", self.options_card)
        self.checkbox_enable_parallel_processing.setObjectName("checkbox_enable_parallel_processing")
        self.checkbox_enable_parallel_processing.setToolTip("Search several files at once in multiple processes")
        self.button_parallel_processing_info = QToolButton(self.options_card)
        self.button_parallel_processing_info.setObjectName("button_parallel_processing_info")
        self.button_parallel_processing_info.setIcon(_icon(theme=QIcon.ThemeIcon.DialogInformation))
        self.button_parallel_processing_info.setText("?")
        self.button_parallel_processing_info.setToolTip("About parallel processing")
        self.button_parallel_processing_info.setAutoRaise(True)
        parallel_row.addWidget(self.checkbox_enable_parallel_processing)
        parallel_row.addWidget(self.button_parallel_processing_info)
        parallel_row.addStretch(1)
        form.addRow(parallel_row)

        limit_row = QHBoxLayout()
        self.checkbox_limit_rows = QCheckBox("Limit results to", self.options_card)
        self.checkbox_limit_rows.setObjectName("checkbox_limit_rows")
        self.checkbox_limit_rows.setToolTip("Stop the search after this many matches")
        self.spinbox_rows = QSpinBox(self.options_card)
        self.spinbox_rows.setObjectName("spinbox_rows")
        self.spinbox_rows.setRange(0, 100_000_000)
        self.spinbox_rows.setSingleStep(1000)
        self.spinbox_rows.setGroupSeparatorShown(True)
        self.spinbox_rows.setSuffix(" rows")
        limit_row.addWidget(self.checkbox_limit_rows)
        limit_row.addWidget(self.spinbox_rows, 1)
        form.addRow(limit_row)

        ol.addLayout(form)
        layout.addWidget(self.options_card, 0)
        return sidebar

    def _build_results_card(self, parent: QWidget) -> QFrame:
        self.results_frame, rl = _card(parent, "results_frame")

        header = QHBoxLayout()
        header.setSpacing(8)
        header.addWidget(_title("Results", self.results_frame))
        self.label_result_count = QLabel("", self.results_frame)
        self.label_result_count.setProperty("role", "badge")
        self.label_result_count.hide()
        header.addWidget(self.label_result_count)
        header.addStretch(1)

        self.button_search_result_export_to_csv = _button(
            "Export…", self.results_frame, variant="accent", icon=QIcon(":/images/export-to-file.png"),
            tooltip="Export the visible rows to Excel or CSV (Ctrl+E)")
        self.button_search_result_export_to_csv.setObjectName("button_search_result_export_to_csv")
        self.button_search_result_clear_results = _button(
            "Clear", self.results_frame, variant="ghost-danger", icon=QIcon(":/images/remove-all.png"),
            tooltip="Clear the results table")
        self.button_search_result_clear_results.setObjectName("button_search_result_clear_results")
        header.addWidget(self.button_search_result_export_to_csv)
        header.addWidget(self.button_search_result_clear_results)
        rl.addLayout(header)

        tools = QHBoxLayout()
        tools.setSpacing(8)
        self.label_filter_text = QLabel("Fil&ter", self.results_frame)
        self.line_edit_filter_table_text = QLineEdit(self.results_frame)
        self.line_edit_filter_table_text.setObjectName("line_edit_filter_table_text")
        self.line_edit_filter_table_text.setPlaceholderText("Type to filter all columns (Ctrl+F)…")
        self.line_edit_filter_table_text.setClearButtonEnabled(True)
        search_icon = _icon(theme=QIcon.ThemeIcon.EditFind)
        if not search_icon.isNull():
            self.line_edit_filter_table_text.addAction(search_icon, QLineEdit.ActionPosition.LeadingPosition)
        self.label_filter_text.setBuddy(self.line_edit_filter_table_text)
        tools.addWidget(self.label_filter_text)
        tools.addWidget(self.line_edit_filter_table_text, 1)
        tools.addSpacing(12)

        self.label_count_occurrences = QLabel("Count by", self.results_frame)
        self.combobox_count_occurrences = QComboBox(self.results_frame)
        self.combobox_count_occurrences.setObjectName("combobox_count_occurrences")
        self.combobox_count_occurrences.setMinimumWidth(140)
        self.combobox_count_occurrences.setToolTip("Column whose values are counted per file")
        self.button_count_occurrences = _button(
            "Count", self.results_frame, tooltip="Show how often each value occurs per file")
        self.button_count_occurrences.setObjectName("button_count_occurrences")
        tools.addWidget(self.label_count_occurrences)
        tools.addWidget(self.combobox_count_occurrences)
        tools.addWidget(self.button_count_occurrences)
        rl.addLayout(tools)

        # Empty state ↔ table
        self.results_stack = QStackedWidget(self.results_frame)
        self.results_empty_state = QLabel(
            "<p style='font-size:13pt;'>No results yet</p>"
            "<p>Choose a folder, add one or more patterns and press <b>Start Search</b> (F5).</p>"
            "<p>Named groups like <code>(?P&lt;user&gt;\\w+)</code> become columns.</p>",
            self.results_stack)
        self.results_empty_state.setObjectName("results_empty_state")
        self.results_empty_state.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.results_empty_state.setWordWrap(True)

        self.table_widget_results = QTableView(self.results_stack)
        self.table_widget_results.setObjectName("table_widget_results")
        self.table_widget_results.setAlternatingRowColors(True)
        self.table_widget_results.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table_widget_results.setWordWrap(False)
        self.table_widget_results.setShowGrid(False)
        self.table_widget_results.setHorizontalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.table_widget_results.verticalHeader().setDefaultSectionSize(26)
        self.table_widget_results.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.table_widget_results.horizontalHeader().setHighlightSections(False)
        self.table_widget_results.horizontalHeader().setStretchLastSection(True)
        self.table_widget_results.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.results_stack.addWidget(self.results_empty_state)
        self.results_stack.addWidget(self.table_widget_results)
        rl.addWidget(self.results_stack, 1)
        return self.results_frame

    def _build_output_card(self, parent: QWidget) -> QFrame:
        self.output_frame, ol = _card(parent, "output_frame")
        header = QHBoxLayout()
        header.addWidget(_title("Output", self.output_frame))
        header.addStretch(1)
        self.label_font_size_program_output = QLabel("Font", self.output_frame)
        self.label_font_size_program_output.setProperty("role", "hint")
        self.combobox_font_size_program_output = QComboBox(self.output_frame)
        self.combobox_font_size_program_output.setObjectName("combobox_font_size_program_output")
        self.combobox_font_size_program_output.addItems(FONT_SIZES)
        self.button_clear_program_output = _button(
            "Clear", self.output_frame, variant="ghost", tooltip="Clear the output log")
        self.button_clear_program_output.setObjectName("button_clear_program_output")
        header.addWidget(self.label_font_size_program_output)
        header.addWidget(self.combobox_font_size_program_output)
        header.addWidget(self.button_clear_program_output)
        ol.addLayout(header)

        self.program_output = QTextEdit(self.output_frame)
        self.program_output.setObjectName("program_output")
        self.program_output.setReadOnly(True)
        self.program_output.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.program_output.setPlaceholderText("Search progress, skipped files and errors appear here…")
        self.program_output.setMinimumHeight(80)
        ol.addWidget(self.program_output, 1)
        return self.output_frame

    # ------------------------------------------------------------------
    # Menus, status bar, shortcuts
    # ------------------------------------------------------------------

    def _build_actions(self, MainWindow: QMainWindow) -> None:
        self.actionOpen_Input_Folder = QAction("Open &Input Folder", MainWindow)
        self.actionOpen_Output_Folder = QAction("Open &Output Folder", MainWindow)
        self.actionExit = QAction("E&xit", MainWindow)
        self.actionExit.setShortcut(QKeySequence.StandardKey.Quit)
        self.actionExit.triggered.connect(MainWindow.close)
        self.actionOpen_Regex_Expression_Manager = QAction("Regex Expression &Manager…", MainWindow)
        self.actionRegex_101 = QAction("Regex &101 (web)", MainWindow)
        self.actionRegex_Cheatsheet = QAction("Regex &Cheatsheet (web)", MainWindow)

    def _build_menus(self, MainWindow: QMainWindow) -> None:
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")

        self.menuOpen = QMenu("&File", self.menubar)
        self.menuOpen.addAction(self.actionOpen_Input_Folder)
        self.menuOpen.addAction(self.actionOpen_Output_Folder)
        self.menuOpen.addSeparator()
        self.menuOpen.addAction(self.actionExit)

        self.menuAutofill = QMenu("&Presets", self.menubar)
        self.menuManage = QMenu("&Manage", self.menubar)
        self.menuManage.addAction(self.actionOpen_Regex_Expression_Manager)
        self.menuHelp = QMenu("&Help", self.menubar)
        self.menuHelp.addAction(self.actionRegex_101)
        self.menuHelp.addAction(self.actionRegex_Cheatsheet)

        for menu in (self.menuOpen, self.menuAutofill, self.menuManage, self.menuHelp):
            self.menubar.addAction(menu.menuAction())
        MainWindow.setMenuBar(self.menubar)

    def _build_statusbar(self, MainWindow: QMainWindow) -> None:
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.setSizeGripEnabled(True)
        self.progress_bar = QProgressBar(self.statusbar)
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFixedWidth(220)
        self.statusbar.addPermanentWidget(self.progress_bar)
        MainWindow.setStatusBar(self.statusbar)

    def _build_shortcuts(self, MainWindow: QMainWindow) -> None:
        def bind(sequence, callback):
            shortcut = QShortcut(QKeySequence(sequence), MainWindow)
            shortcut.setContext(Qt.ShortcutContext.WindowShortcut)
            shortcut.activated.connect(callback)
            return shortcut

        self._shortcuts = [
            bind("F5", self.button_start_search.click),
            bind("Ctrl+Return", self.button_start_search.click),
            bind("Ctrl+O", self.button_browse_folder.click),
            bind("Ctrl+E", self.button_search_result_export_to_csv.click),
            bind("Ctrl+F", lambda: (self.line_edit_filter_table_text.setFocus(),
                                    self.line_edit_filter_table_text.selectAll())),
            bind("Ctrl+L", self.line_edit_regex.setFocus),
        ]
        delete = QShortcut(QKeySequence.StandardKey.Delete, self.list_widget_regex)
        delete.setContext(Qt.ShortcutContext.WidgetShortcut)
        delete.activated.connect(self.button_regex_pattern_remove_selected.click)
        self._shortcuts.append(delete)

    def _set_tab_order(self, MainWindow: QMainWindow) -> None:
        order = [
            self.line_edit_files_folder, self.button_browse_folder, self.line_edit_file_pattern,
            self.button_start_search, self.line_edit_string_to_regex, self.button_string_to_regex,
            self.line_edit_regex, self.button_add_regex_to_list_widget, self.list_widget_regex,
            self.combobox_segmentation_mode, self.checkbox_multiline_search,
            self.checkbox_enable_parallel_processing, self.checkbox_limit_rows, self.spinbox_rows,
            self.line_edit_filter_table_text, self.combobox_count_occurrences,
            self.button_count_occurrences, self.table_widget_results,
        ]
        for first, second in zip(order, order[1:]):
            MainWindow.setTabOrder(first, second)
