# File: modules/excel_exporter.py
from PySide6.QtCore import QObject, Signal, QRunnable, Slot
from PySide6.QtGui import QIcon
import pandas as pd


class ExcelExporterSignals(QObject):
    message_information = Signal(str, str)
    message_warning = Signal(str, str)
    message_critical = Signal(str, str)
    statusbar_show_message = Signal(str, int)
    export_success_with_path = Signal(str, object)

class ExcelExporterThread(QRunnable):
    def __init__(self, data: list[list], headers: list[str], output_file_path: str, app_icon: QIcon):
        super().__init__()
        self.signals = ExcelExporterSignals()
        self.data = data
        self.headers = headers
        self.output_file_path: str = output_file_path
        self.app_icon = app_icon
        self.setAutoDelete(True)

    def set_file_path(self, file_path: str):
        """Called from main thread once user selects file"""
        self.output_file_path = file_path

    @Slot()
    def run(self):
        try:
            if not self.data:
                self.signals.message_critical.emit("Data Validation Error", "No data to export.")
                return
            if not self.headers:
                self.signals.message_critical.emit("Data Validation Error", "No header found from table.")
                return

            # Wait until path is set
            if not self.output_file_path:
                raise ValueError("File path was not provided.") # user canceled or missing

            if not self.output_file_path.lower().endswith(".xlsx"):
                self.output_file_path += ".xlsx"

            # Export to Excel
            df = pd.DataFrame(self.data, columns=self.headers)
            self.signals.statusbar_show_message.emit(f"Exporting to Excel file in: {self.output_file_path}", 10000)
            df.to_excel(self.output_file_path, index=False)

            self.signals.export_success_with_path.emit(self.output_file_path, self.app_icon)
            self.signals.statusbar_show_message.emit("Result exported to Excel.", 5000)

        except Exception as e:
            self.signals.message_critical.emit("Thread Export Error", f"Thread error: {str(e)}")
