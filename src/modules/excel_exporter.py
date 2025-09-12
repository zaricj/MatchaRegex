from PySide6.QtCore import QObject, Signal, QRunnable, Slot
import pandas as pd

class ExcelExporterSignals(QObject):
    message_information = Signal(str, str)
    message_warning = Signal(str, str)
    message_critical = Signal(str, str)
    statusbar_show_message = Signal(str, int)
    request_save_file_path = Signal() 
    export_success_with_path = Signal(str)

class ExcelExporterThread(QRunnable):
    def __init__(self, data: list[list], headers: list[str], main_window):
        super().__init__()
        self.signals = ExcelExporterSignals()
        self.data = data # Data to convert to excel
        self.headers = headers # The table headers
        self.main_window = main_window  # Reference to main window for file dialog
        self.setAutoDelete(True)

    @Slot()
    def run(self):
        try:
            # Check if any data even exists
            if not self.data:
                self.signals.message_critical.emit("Data Validation Error", "No data to export.")
                return
            elif not self.headers:
                self.signals.message_critical.emit("Data Validation Error", "No header found from table.")
                return
            
            # Convert data to a pandas DataFrame
            df = pd.DataFrame(self.data, columns=self.headers)
            
            # Import here to avoid circular imports
            from PySide6.QtWidgets import QFileDialog
            
            # Show file dialog in main thread (this is safe to call from worker thread)
            file_path, _ = QFileDialog.getSaveFileName(
                self.main_window,
                "Export Result", 
                "Regex_Search_Result", 
                "Excel Files (*.xlsx)"
            )
            
            if not file_path:
                return  # User cancelled
                
            if not file_path.lower().endswith('.xlsx'):
                file_path += '.xlsx'
            
            # Export to Excel
            df.to_excel(file_path, index=False)
            self.signals.export_success_with_path.emit(file_path)
            self.signals.statusbar_show_message.emit("Result exported to Excel.", 5000)
            
        except Exception as e:
            self.signals.message_critical.emit("Thread Export Error", f"Thread error: {str(e)}")