# File: modules/excel_exporter.py
from PySide6.QtCore import QObject, Signal, Qt
from PySide6.QtGui import QIcon
import pandas as pd


class ExcelExporterSignals(QObject):
    message_information = Signal(str, str)
    message_warning = Signal(str, str)
    message_critical = Signal(str, str)
    statusbar_show_message = Signal(str, int)
    export_success_with_path = Signal(str, object)


def export_table_to_excel(table, row_count: int, col_count: int, output_file_path: str,
                          app_icon: QIcon, signals: ExcelExporterSignals | None = None):
    worker_signals = signals or ExcelExporterSignals()

    try:
        if not output_file_path:
            raise ValueError("File path was not provided.")

        worker_signals.statusbar_show_message.emit(
            "Preparing data for export, please wait...", 0)
        data = []
        headers = []
        model = table.model()

        for row in range(row_count):
            if table.isRowHidden(row):
                continue

            row_data = []
            for col in range(col_count):
                if row == 0:
                    headers.append(model.headerData(col, Qt.Horizontal))
                index = model.index(row, col)
                cell_data = model.data(index)
                row_data.append(cell_data if cell_data else "")
            data.append(row_data)

        if not data:
            worker_signals.message_critical.emit(
                "Data Validation Error", "No data to export.")
            return

        if not headers:
            worker_signals.message_critical.emit(
                "Data Validation Error", "No headers found for export.")
            return

        if not output_file_path.lower().endswith(".xlsx"):
            output_file_path += ".xlsx"

        df = pd.DataFrame(data, columns=headers)
        worker_signals.statusbar_show_message.emit(
            f"Exporting data to Excel file in file: {output_file_path}", 10000)

        with pd.ExcelWriter(output_file_path, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Result", index=False)
            worksheet = writer.sheets["Result"]
            max_row, max_col = df.shape
            column_settings = [{"header": col} for col in df.columns]
            worksheet.add_table(0, 0, max_row, max_col - 1, {
                "columns": column_settings,
                "style": "Table Style Medium 16",
                "name": f"{"Result"[:30]}",
                "autofilter": True
            })
            worksheet.set_column(0, max_col - 1, 18)

        worker_signals.export_success_with_path.emit(
            output_file_path, app_icon)
        worker_signals.statusbar_show_message.emit(
            "Result exported to Excel.", 5000)

    except Exception as e:
        worker_signals.message_critical.emit(
            "Thread Export Error", f"Thread error: {str(e)}")
