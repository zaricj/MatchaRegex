"""
Thread-safe export of result rows to CSV or Excel.

The GUI takes a *snapshot* (column list + list of row dicts) and hands it to
a background worker — no Qt widget/model is ever touched off the GUI thread.

Safety:
* Excel: ``strings_to_formulas`` is disabled, so log content such as
  ``=HYPERLINK(...)`` is written as plain text, never as a live formula.
* CSV: cells that Excel would interpret as a formula are prefixed with ``'``
  (OWASP "CSV injection" mitigation); plain numbers such as ``-5`` are kept.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any, Sequence

from PySide6.QtCore import QObject, Signal

EXCEL_MAX_ROWS = 1_048_576 - 1          # minus header row
EXCEL_MAX_CELL_CHARS = 32_767
EXCEL_TABLE_STYLE = "Table Style Medium 16"

_FORMULA_PREFIXES = ("=", "+", "-", "@", "\t", "\r")
_PLAIN_NUMBER = re.compile(r"[+-]?\d+(?:[.,]\d+)?")


class ExportSignals(QObject):
    status = Signal(str, int)            # statusbar message, timeout
    failed = Signal(str, str)            # title, message
    succeeded = Signal(str)              # final file path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _unique_headers(columns: Sequence[str]) -> list[str]:
    """Excel tables need unique, case-insensitive headers."""
    seen: set[str] = set()
    headers: list[str] = []
    for col in columns:
        name = str(col) or "Column"
        candidate, n = name, 2
        while candidate.lower() in seen:
            candidate = f"{name} ({n})"
            n += 1
        seen.add(candidate.lower())
        headers.append(candidate)
    return headers


def _csv_safe(value: Any) -> Any:
    if isinstance(value, str) and value.startswith(_FORMULA_PREFIXES) and not _PLAIN_NUMBER.fullmatch(value):
        return "'" + value
    return value


def _xlsx_cell(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return value
    text = str(value)
    return text if len(text) <= EXCEL_MAX_CELL_CHARS else text[: EXCEL_MAX_CELL_CHARS - 1] + "…"


# ---------------------------------------------------------------------------
# Writers
# ---------------------------------------------------------------------------

def write_csv(path: Path, columns: Sequence[str], rows: Sequence[dict], delimiter: str = ",") -> None:
    """utf-8-sig so Excel detects UTF-8; DictWriter keeps every value in its column."""
    with open(path, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=list(columns),
            delimiter=delimiter,
            extrasaction="ignore",
            restval="",
            quoting=csv.QUOTE_MINIMAL,
        )
        writer.writeheader()
        for row in rows:
            writer.writerow({c: _csv_safe(row.get(c, "")) for c in columns})


def write_xlsx(path: Path, columns: Sequence[str], rows: Sequence[dict]) -> None:
    import xlsxwriter

    headers = _unique_headers(columns)
    workbook = xlsxwriter.Workbook(
        str(path),
        {"strings_to_formulas": False, "strings_to_urls": False, "strings_to_numbers": False},
    )
    try:
        chunks = [rows[i:i + EXCEL_MAX_ROWS] for i in range(0, len(rows), EXCEL_MAX_ROWS)] or [[]]
        for number, chunk in enumerate(chunks, start=1):
            name = "Result" if number == 1 else f"Result_{number}"
            sheet = workbook.add_worksheet(name)
            data = [[_xlsx_cell(row.get(c, "")) for c in columns] for row in chunk]
            if data:
                sheet.add_table(0, 0, len(data), len(headers) - 1, {
                    "data": data,
                    "columns": [{"header": h} for h in headers],
                    "style": EXCEL_TABLE_STYLE,
                    "name": name,
                    "autofilter": True,
                })
            else:
                sheet.write_row(0, 0, headers)
            # Width from header + first rows, clamped.
            for col_idx, header in enumerate(headers):
                sample = [len(str(r[col_idx])) for r in data[:200]]
                width = max([len(header), *sample]) + 2
                sheet.set_column(col_idx, col_idx, min(max(width, 8), 60))
            sheet.freeze_panes(1, 0)
    finally:
        workbook.close()


# ---------------------------------------------------------------------------
# Worker entry point (run through services.workers.thread_worker.Worker)
# ---------------------------------------------------------------------------

def export_results(
    output_path: str,
    columns: list[str],
    rows: list[dict],
    csv_delimiter: str | None = None,
    signals: ExportSignals | None = None,
) -> None:
    """
    ``csv_delimiter`` given → CSV, otherwise Excel (.xlsx).
    The extension is fixed up to match the chosen format.
    """
    signals = signals or ExportSignals()
    try:
        if not output_path:
            raise ValueError("No output file path given.")
        if not columns or not rows:
            signals.failed.emit("Export", "There is no data to export.")
            return

        path = Path(output_path)
        wanted_suffix = ".csv" if csv_delimiter else ".xlsx"
        if path.suffix.lower() != wanted_suffix:
            path = path.with_name(path.name + wanted_suffix)

        signals.status.emit(f"Exporting {len(rows)} rows to {path} ...", 0)
        if csv_delimiter:
            write_csv(path, columns, rows, csv_delimiter)
        else:
            if len(rows) > EXCEL_MAX_ROWS:
                signals.status.emit(
                    f"More than {EXCEL_MAX_ROWS} rows — splitting across multiple worksheets ...", 0)
            write_xlsx(path, columns, rows)

        signals.status.emit("Export finished.", 5000)
        signals.succeeded.emit(str(path))
    except PermissionError:
        signals.failed.emit(
            "Export Failed",
            f"Could not write the file:\n{output_path}\n\nIs it currently open in Excel or another program?",
        )
    except Exception as exc:
        signals.failed.emit("Export Failed", f"{type(exc).__name__}: {exc}")
