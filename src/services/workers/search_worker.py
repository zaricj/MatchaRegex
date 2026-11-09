from __future__ import annotations

import threading
import time
import traceback
from dataclasses import asdict

from PySide6.QtCore import QObject, QThread, Signal

from core.search.engine import PatternError, SearchOptions, run_search


class SearchWorker(QThread):
    """
    Runs :func:`core.search.engine.run_search` off the GUI thread.

    All communication happens through signals (queued into the GUI thread).
    Rows and log lines are buffered and flushed at most every
    ``FLUSH_INTERVAL`` seconds / ``FLUSH_ROWS`` rows so the GUI event loop is
    never flooded with one signal per match or per file.
    """

    schema_ready = Signal(list)          # column names (locked schema)
    rows_ready = Signal(list)            # batch of row dicts
    progress_changed = Signal(int)       # percent 0..100
    log_message = Signal(str)            # one or more lines
    search_failed = Signal(str, str)     # title, message
    search_completed = Signal(dict)      # SearchSummary as dict

    FLUSH_INTERVAL = 0.15
    FLUSH_ROWS = 5000

    def __init__(self, options: SearchOptions, workers: int = 1, parent: QObject | None = None):
        super().__init__(parent)
        self._options = options
        self._workers = max(1, workers)
        self._stop = threading.Event()
        self._row_buffer: list[dict] = []
        self._log_buffer: list[str] = []
        self._last_flush = 0.0
        self._last_percent = -1

    # Called from the GUI thread.
    def cancel(self) -> None:
        self._stop.set()

    def is_cancelled(self) -> bool:
        return self._stop.is_set()

    # ----- worker thread -----

    def _flush(self, force: bool = False) -> None:
        now = time.monotonic()
        if not force and now - self._last_flush < self.FLUSH_INTERVAL and len(self._row_buffer) < self.FLUSH_ROWS:
            return
        self._last_flush = now
        if self._log_buffer:
            self.log_message.emit("\n".join(self._log_buffer))
            self._log_buffer = []
        if self._row_buffer:
            self.rows_ready.emit(self._row_buffer)
            self._row_buffer = []

    def _on_rows(self, rows: list[dict]) -> None:
        self._row_buffer.extend(rows)
        self._flush()

    def _on_log(self, text: str) -> None:
        self._log_buffer.append(text)
        self._flush()

    def _on_progress(self, done: int, total: int) -> None:
        percent = int(done * 100 / total) if total else 100
        if percent != self._last_percent:
            self._last_percent = percent
            self.progress_changed.emit(percent)
        self._flush()

    def run(self) -> None:
        summary: dict = {}
        try:
            result = run_search(
                self._options,
                on_schema=self.schema_ready.emit,
                on_rows=self._on_rows,
                on_progress=self._on_progress,
                on_log=self._on_log,
                should_stop=self._stop.is_set,
                workers=self._workers,
            )
            summary = asdict(result)
        except PatternError as exc:
            self.search_failed.emit("Regex Error", str(exc))
        except ValueError as exc:
            self.search_failed.emit("Search Error", str(exc))
        except Exception as exc:  # never let an exception kill the thread silently
            self._log_buffer.append(traceback.format_exc())
            self.search_failed.emit("Fatal Search Error", f"{type(exc).__name__}: {exc}")
        finally:
            self._flush(force=True)
            self.search_completed.emit(summary)
