"""
Two-column list of active search patterns:  Header(s) | Regex.

* Patterns **with** named groups show their group names – those become the
  CSV/Excel columns automatically (read-only here).
* Patterns **without** named groups have one editable header (default
  ``Match``). Double-click or F2 to rename it.

Offers the subset of the ``QListWidget`` API used by ``app.MainWindow``
(``currentRow``, ``takeItem``, ``count``, ``clear``) so both layouts share the
same logic.
"""
from __future__ import annotations

import re

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QKeyEvent
from PySide6.QtWidgets import QAbstractItemView, QHeaderView, QTreeWidget, QTreeWidgetItem, QWidget

DEFAULT_HEADER = "Match"
COL_HEADER, COL_REGEX = 0, 1
_EDITABLE_ROLE = Qt.ItemDataRole.UserRole + 1


class PatternListWidget(QTreeWidget):
    header_edited = Signal(int, str)  # row, new header ("" = default)

    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        self.setColumnCount(2)
        self.setHeaderLabels(["Column header", "Regex"])
        self.setRootIsDecorated(False)
        self.setUniformRowHeights(True)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)  # handled manually per column
        self.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        header = self.header()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(COL_HEADER, QHeaderView.ResizeMode.Interactive)
        header.resizeSection(COL_HEADER, 120)
        header.setHighlightSections(False)

        self.itemDoubleClicked.connect(self._on_double_clicked)
        self.itemChanged.connect(self._on_item_changed)

    # ----- QListWidget-compatible API -----

    def count(self) -> int:
        return self.topLevelItemCount()

    def currentRow(self) -> int:
        item = self.currentItem()
        return self.indexOfTopLevelItem(item) if item is not None else -1

    def takeItem(self, row: int) -> QTreeWidgetItem | None:
        return self.takeTopLevelItem(row)

    # ----- patterns -----

    def add_pattern(self, name: str, expression: str, header: str = "") -> None:
        try:
            groups = list(re.compile(expression).groupindex)
        except re.error:
            groups = []

        item = QTreeWidgetItem()
        item.setText(COL_REGEX, expression)
        item.setToolTip(COL_REGEX, f"{name}\n{expression}")
        mono = QFont()
        mono.setFamilies(["Cascadia Mono", "Consolas", "Courier New"])
        mono.setStyleHint(QFont.StyleHint.Monospace)
        item.setFont(COL_REGEX, mono)

        if groups:
            item.setText(COL_HEADER, ", ".join(groups))
            item.setToolTip(COL_HEADER, "Named groups (?P<name>…) are used as column headers.")
            item.setData(COL_HEADER, _EDITABLE_ROLE, False)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)
        else:
            item.setText(COL_HEADER, header.strip() or DEFAULT_HEADER)
            item.setToolTip(COL_HEADER, "Column header for this pattern's matches.\nDouble-click or F2 to rename.")
            item.setData(COL_HEADER, _EDITABLE_ROLE, True)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsEditable)
            font = item.font(COL_HEADER)
            font.setItalic(not header.strip())
            item.setFont(COL_HEADER, font)

        self.blockSignals(True)
        self.addTopLevelItem(item)
        self.blockSignals(False)

    def edit_header(self, item: QTreeWidgetItem | None = None) -> None:
        item = item or self.currentItem()
        if item is not None and item.data(COL_HEADER, _EDITABLE_ROLE):
            self.editItem(item, COL_HEADER)

    # ----- events -----

    def _on_double_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        if column == COL_HEADER:
            self.edit_header(item)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_F2:
            self.edit_header()
            return
        super().keyPressEvent(event)

    def _on_item_changed(self, item: QTreeWidgetItem, column: int) -> None:
        if column != COL_HEADER or not item.data(COL_HEADER, _EDITABLE_ROLE):
            return
        text = item.text(COL_HEADER).strip()
        header = "" if text in ("", DEFAULT_HEADER) else text
        self.blockSignals(True)
        item.setText(COL_HEADER, header or DEFAULT_HEADER)
        font = item.font(COL_HEADER)
        font.setItalic(not header)
        item.setFont(COL_HEADER, font)
        self.blockSignals(False)
        self.header_edited.emit(self.indexOfTopLevelItem(item), header)
