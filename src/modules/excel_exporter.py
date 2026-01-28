# File: modules/excel_exporter.py
from PySide6.QtCore import QObject, Signal, QRunnable, Slot, Qt
from PySide6.QtGui import QIcon
import pandas as pd


class ExcelExporterSignals(QObject):
    message_information = Signal(str, str)
    message_warning = Signal(str, str)
    message_critical = Signal(str, str)
    statusbar_show_message = Signal(str, int)
    export_success_with_path = Signal(str, object)


class ExcelExporterThread(QRunnable):
    def __init__(self, table, row_count: int, col_count: int, output_file_path: str, app_icon: QIcon):
        super().__init__()
        self.signals = ExcelExporterSignals()
        self.table = table
        self.row_count = row_count
        self.col_count = col_count
        self.output_file_path: str = output_file_path
        self.app_icon = app_icon
        self.setAutoDelete(True)

    def set_file_path(self, file_path: str):
        """Called from main thread once user selects file"""
        self.output_file_path = file_path

    @Slot()
    def run(self):
        try:
            # Wait until path is set
            if not self.output_file_path:
                # user canceled or missing
                raise ValueError("File path was not provided.")

            # Extract data from table (in background thread)
            self.signals.statusbar_show_message.emit(
                "Preparing data for export, please wait...", 0)
            data = []
            headers = []
            for row in range(self.row_count):
                # Skip hidden rows when using a text filter
                if self.table.isRowHidden(row):
                    continue
                row_data = []
                model = self.table.model()
                for col in range(self.col_count):
                    if row == 0: # Get headers
                        headers.append(model.headerData(col, Qt.Horizontal))
                    index = model.index(row, col)
                    cell_data = model.data(index)
                    row_data.append(cell_data if cell_data else "")
                data.append(row_data)
                

            if not data:
                self.signals.message_critical.emit(
                    "Data Validation Error", "No data to export.")
                return
            
            if not headers:
                self.signals.message_critical.emit(
                    "Data Validation Error", "No headers found for export.")
                return

            if not self.output_file_path.lower().endswith(".xlsx"):
                self.output_file_path += ".xlsx"

            # Export to Excel
            df = pd.DataFrame(data, columns=headers)
            self.signals.statusbar_show_message.emit(
                f"Exporting data to Excel file in file: {self.output_file_path}", 10000)

            with pd.ExcelWriter(self.output_file_path, engine="xlsxwriter") as writer:
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

            self.signals.export_success_with_path.emit(
                self.output_file_path, self.app_icon)
            self.signals.statusbar_show_message.emit(
                "Result exported to Excel.", 5000)

        except Exception as e:
            self.signals.message_critical.emit(
                "Thread Export Error", f"Thread error: {str(e)}")
