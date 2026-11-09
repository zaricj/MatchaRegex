import itertools
import os
import subprocess
import sys
from pathlib import Path

from PySide6.QtCore import QObject, Signal
from PySide6.QtWidgets import QFileDialog, QLineEdit

from gui.ui.main.LogSearcherUI_ui import Ui_MainWindow

# Counting files is done on the GUI thread, so stop early on huge trees.
_FILE_COUNT_CAP = 10_000


class HelperMethodSignals(QObject):
    program_output_text = Signal(str)          # Emitted for program output
    statusbar_show_message = Signal(str, int)  # (message, timeout)


class HelperMethods:
    def __init__(self, main_window=None):
        self.main_window = main_window
        self.ui: Ui_MainWindow = main_window.ui
        self.signals = HelperMethodSignals()

    def browse_folder_path(self, line_edit: QLineEdit):
        folder_path = QFileDialog.getExistingDirectory(
            self.main_window,
            "Select Folder",
            line_edit.text().strip(),
            QFileDialog.Option.ShowDirsOnly | QFileDialog.Option.DontResolveSymlinks,
        )
        if folder_path:
            line_edit.setText(folder_path)  # textChanged → show_relevant_info

    def show_relevant_info(self, folder_path: str) -> None:
        """Show how many files the current folder + file patterns would search."""
        path = Path(folder_path.strip()) if folder_path.strip() else None
        if path is None or not path.is_dir():
            return

        patterns = [p.strip() for p in self.ui.line_edit_file_pattern.text().split(",") if p.strip()]
        try:
            found: set[Path] = set()
            for pattern in patterns or ["*"]:
                remaining = _FILE_COUNT_CAP + 1 - len(found)
                if remaining <= 0:
                    break
                found.update(p for p in itertools.islice(path.glob(pattern), remaining))
        except (ValueError, NotImplementedError, OSError) as exc:
            self.signals.statusbar_show_message.emit(f"Invalid file pattern: {exc}", 8000)
            return

        count = f"{_FILE_COUNT_CAP}+" if len(found) > _FILE_COUNT_CAP else str(len(found))
        suffix = f" | Patterns: {', '.join(patterns)}" if patterns else ""
        self.signals.statusbar_show_message.emit(f"Selected folder: {path} | Matching entries: {count}{suffix}", 20000)

    def open_dir_in_file_manager(self, folder_path: str) -> None:
        """Open a folder in the OS file manager (Windows, macOS, Linux)."""
        if not folder_path:
            self.signals.statusbar_show_message.emit("Please set the folder path in the specific input field first!", 6000)
            return
        path = Path(folder_path)
        if not path.is_dir():
            self.signals.statusbar_show_message.emit(f"Folder does not exist: {path}", 6000)
            return
        try:
            if sys.platform == "win32":
                os.startfile(path)  # noqa: S606 — opens a directory, not a user supplied command
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                subprocess.Popen([opener, str(path)])  # non-blocking, no shell
        except Exception as ex:
            self.signals.program_output_text.emit(
                f"Could not open directory in file manager ({type(ex).__name__}): {ex}")
