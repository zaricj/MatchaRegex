import inspect
import sys
import traceback

from PySide6.QtCore import QObject, QRunnable, Signal, Slot


class WorkerSignals(QObject):
    finished = Signal()
    error = Signal(tuple)
    result = Signal(object)
    progress = Signal(int)


class Worker(QRunnable):
    """Generic worker for offloading callables to the Qt thread pool."""

    def __init__(self, fn, *args, signals_factory=None, **kwargs):
        super().__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = signals_factory() if signals_factory else WorkerSignals()
        self._auto_emit_base_signals = signals_factory is None
        self._is_running = False
        self._stop_requested = False
        self.setAutoDelete(True)

        try:
            fn_signature = inspect.signature(self.fn)
        except (TypeError, ValueError):
            fn_signature = None

        if fn_signature and "signals" in fn_signature.parameters:
            self.kwargs.setdefault("signals", self.signals)

        if fn_signature and "progress_callback" in fn_signature.parameters:
            progress_signal = getattr(
                self.signals,
                "progress",
                getattr(self.signals, "progress_update", None),
            )
            if progress_signal is not None:
                self.kwargs.setdefault("progress_callback", progress_signal)

        if fn_signature and "stop_requested" in fn_signature.parameters:
            self.kwargs.setdefault("stop_requested", lambda: self._stop_requested)

    def isRunning(self) -> bool:
        return self._is_running

    def stop(self):
        self._stop_requested = True

    @Slot()
    def run(self):
        self._is_running = True
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            if self._auto_emit_base_signals:
                self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            if self._auto_emit_base_signals:
                self.signals.result.emit(result)
        finally:
            self._is_running = False
            if self._auto_emit_base_signals:
                self.signals.finished.emit()
