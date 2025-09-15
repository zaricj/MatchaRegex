from resources.interface.LogSearcherUI_ui import Ui_MainWindow
from PySide6.QtWidgets import QFileDialog, QLineEdit
from PySide6.QtCore import QObject, Signal
import os
import sys
import subprocess
from pathlib import Path


class HelperMethodSignals(QObject):
    program_output_text = Signal(str)         # Emitted for program output
    statusbar_show_message = Signal(str, int) # Emitted to show message in status bar (message, timeout)

class HelperMethods:
    def __init__(self, main_window=None):
        self.main_window = main_window
        self.ui: Ui_MainWindow = main_window.ui
        self.signals = HelperMethodSignals()
        
    def browse_folder_path(self, line_edit: QLineEdit):
        folder_path = QFileDialog.getExistingDirectory(
            self.main_window,
            "Select Folder",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks,
        )
        if folder_path:
            line_edit.setText(folder_path)
            self.show_relevant_info(folder_path=line_edit.text())
    
    def input_field_text_changed(self, line_edit: QLineEdit) -> None:
        """On input field text change, this method gets triggered. It runs the 'show_relevant_info' method

        Args:
            line_edit (QLineEdit): The input field to look for
        """
        self.show_relevant_info(folder_path=line_edit.text())
    
    def show_relevant_info(self, folder_path: str) -> None:
        """Prints out the relevant info based on browse button press or just text changed in the specified input field

        Args:
            folder_path (str): Path of the folder which is grabbed from the QFileDialog window.
        """
        path = Path(folder_path)
        if path.exists() and path.is_dir():
            
            files = []
            file_patterns = self.ui.line_edit_file_pattern.text().strip().split(",")

            # Fixed: Check if file_patterns is not empty and contains valid patterns
            if file_patterns and file_patterns != ['']:
                self.signals.program_output_text.emit(f"Using file patterns: {file_patterns}")

                for pattern in file_patterns:
                    pattern = pattern.strip()
                    if pattern:
                        files.extend(path.glob(pattern))
                        self.signals.program_output_text.emit(f"Pattern '{pattern}' matched {len(list(path.glob(pattern)))} files.")
                if len(files) > 0:
                    self.signals.statusbar_show_message.emit(f"Selected folder: {folder_path} | Total files: {len(files)} | Using patterns: {file_patterns}", 10000)
            else:
                files = list(path.glob('*.*'))
                if len(files) > 0:
                    self.signals.statusbar_show_message.emit(f"Selected folder: {folder_path} | Total files: {len(files)}", 10000)
                    
    def open_dir_in_file_manager(self, folder_path: str) -> None:
        """Opens the specified folder path in the file system manager. OS cross-platform independent, support Windows, Linux and macOS.  

        Args:
            folder_path (str): Folder path to open in the file system manager.
        """
        try:
            if folder_path != "":
                path = Path(folder_path)
                if sys.platform == "win32":
                    os.startfile(path)
                else:
                    opener = "open" if sys.platform == "darwin" else "xdg-open"
                    subprocess.call([opener, path])
        except Exception as ex:
            msg: str = f"Exception {type(ex).__name__}, could not open directory in file system manager, error message: {str(ex)}"
            self.signals.program_output_text.emit(msg)