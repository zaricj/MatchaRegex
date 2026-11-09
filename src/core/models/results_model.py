from __future__ import annotations

from typing import Any, Iterable

from PySide6.QtCore import QAbstractTableModel, QModelIndex, QObject, Qt


class ResultsTableModel(QAbstractTableModel):
    """
    Table model backed by a list of row dicts and a locked column schema.

    Rows are looked up by column *name*, never by position, so rows produced by
    different patterns (with different named groups) can never shift columns.
    Rows are appended in batches from the search worker.
    """

    def __init__(self, columns: Iterable[str] = (), rows: Iterable[dict] = (), parent: QObject | None = None):
        super().__init__(parent)
        self._columns: list[str] = list(columns)
        self._rows: list[dict[str, Any]] = list(rows)

    # ----- public API -----

    def columns(self) -> list[str]:
        return list(self._columns)

    def rows(self) -> list[dict[str, Any]]:
        """Shallow copy — safe to hand to a background thread."""
        return list(self._rows)

    def row_at(self, row: int) -> dict[str, Any]:
        return self._rows[row]

    def reset(self, columns: Iterable[str] = (), rows: Iterable[dict] = ()) -> None:
        self.beginResetModel()
        self._columns = list(columns)
        self._rows = list(rows)
        self.endResetModel()

    def append_rows(self, rows: list[dict[str, Any]]) -> None:
        if not rows:
            return
        # Defensive: unknown keys get a column instead of being silently lost.
        known = set(self._columns)
        extra = [k for row in rows for k in row if k not in known and not known.add(k)]
        if extra:
            start = len(self._columns)
            self.beginInsertColumns(QModelIndex(), start, start + len(extra) - 1)
            self._columns.extend(extra)
            self.endInsertColumns()

        first = len(self._rows)
        self.beginInsertRows(QModelIndex(), first, first + len(rows) - 1)
        self._rows.extend(rows)
        self.endInsertRows()

    # ----- Qt model interface -----

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._rows)

    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return 0 if parent.isValid() else len(self._columns)

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        if role in (Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.ToolTipRole):
            value = self._rows[index.row()].get(self._columns[index.column()], "")
            if role == Qt.ItemDataRole.ToolTipRole:
                text = str(value)
                return text if len(text) > 60 else None
            return value  # ints stay ints → numeric sorting for Line/Column
        return None

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return self._columns[section] if 0 <= section < len(self._columns) else None
        return section + 1
