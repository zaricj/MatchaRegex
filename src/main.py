import multiprocessing
import sys


def main() -> int:
    # Imported lazily: worker processes (spawn) re-import this module and must
    # not load the whole GUI stack.
    from PySide6.QtWidgets import QApplication

    from app import MainWindow

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    # Required for the search worker processes in a compiled (Nuitka) build.
    multiprocessing.freeze_support()
    raise SystemExit(main())
