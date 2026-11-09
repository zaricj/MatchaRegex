"""
Regex search engine.

Pure Python — deliberately **no Qt imports** — so that it can run
inside worker *processes*.  Files are searched in a ``ProcessPoolExecutor``:

* Python's ``re`` module holds the GIL while matching, so threads give no real
  parallelism and a catastrophic-backtracking pattern in a thread would freeze
  the whole GUI.  A process can be terminated, so "Stop" always works.
* ``workers=1`` is the sequential mode, ``workers>1`` the parallel mode.

Every result row follows one locked schema (see :func:`build_schema`) so that
the table, CSV and Excel output can never drift out of alignment.
"""
from __future__ import annotations

import codecs
import multiprocessing
import re
import time
from concurrent.futures import FIRST_COMPLETED, Future, ProcessPoolExecutor, wait
from concurrent.futures.process import BrokenProcessPool
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

from core.search.segmenters import iter_blocks

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

BASE_COLUMNS: tuple[str, ...] = ("File", "Line", "Column", "Pattern")
MATCH_COLUMN = "Match"
_RESERVED = {c.lower() for c in (*BASE_COLUMNS, MATCH_COLUMN)}

# ---------------------------------------------------------------------------
# Tuning
# ---------------------------------------------------------------------------

SNIFF_SIZE = 64 * 1024                        # bytes used for encoding detection
WHOLE_FILE_MAX_BYTES = 256 * 1024 * 1024      # larger files fall back to segments
_LINE_BREAKS = re.compile(r"\r\n|\r|\n")

RowDict = dict[str, Any]


class PatternError(ValueError):
    """Raised when a user supplied regex does not compile."""

    def __init__(self, name: str, message: str):
        super().__init__(f"Invalid regex pattern '{name}': {message}")
        self.pattern_name = name


@dataclass(frozen=True, slots=True)
class PatternDef:
    """Picklable pattern definition sent to worker processes."""
    name: str
    expression: str
    header: str = ""      # column header for patterns *without* named groups ("" → "Match")


@dataclass(frozen=True, slots=True)
class CompiledPattern:
    name: str
    regex: re.Pattern
    group_columns: tuple[tuple[str, str], ...]   # (group name, column name)
    match_column: str = MATCH_COLUMN               # used when there are no named groups


@dataclass(frozen=True, slots=True)
class SearchOptions:
    folder: Path
    patterns: tuple[PatternDef, ...]
    file_patterns: tuple[str, ...] = ()
    segmentation_mode: str = "Auto"
    whole_file: bool = False          # "multiline" search: one block per file
    max_rows: int = 0                 # 0 = unlimited


@dataclass(slots=True)
class FileResult:
    file_label: str
    rows: list[RowDict] = field(default_factory=list)
    error: str | None = None
    note: str | None = None


@dataclass(slots=True)
class SearchSummary:
    total_files: int = 0
    searched_files: int = 0
    total_rows: int = 0
    failed_files: int = 0
    cancelled: bool = False
    limit_reached: bool = False
    elapsed: float = 0.0


# ---------------------------------------------------------------------------
# Pattern compilation
# ---------------------------------------------------------------------------

def _column_for_group(group: str) -> str:
    """Avoid named groups overwriting metadata columns (``File``, ``Line`` ...)."""
    return f"{group} (group)" if group.lower() in _RESERVED else group


def match_column_for(header: str) -> str:
    """Column for the full match of a pattern without named groups."""
    header = (header or "").strip()
    if not header or header == MATCH_COLUMN:
        return MATCH_COLUMN
    return _column_for_group(header)


def compile_patterns(patterns: Iterable[PatternDef]) -> list[CompiledPattern]:
    """Compile once, before any file is touched. Raises :class:`PatternError`."""
    compiled: list[CompiledPattern] = []
    for spec in patterns:
        try:
            regex = re.compile(spec.expression, re.MULTILINE)
        except re.error as exc:
            raise PatternError(spec.name, str(exc)) from exc
        groups = tuple((g, _column_for_group(g)) for g in regex.groupindex)
        compiled.append(CompiledPattern(spec.name, regex, groups, match_column_for(spec.header)))
    return compiled


def build_schema(compiled: Sequence[CompiledPattern]) -> list[str]:
    """
    Locked column order: metadata columns, then named groups / custom headers
    in pattern order, then ``Match`` if any pattern without named groups has
    no custom header.
    """
    columns: list[str] = list(BASE_COLUMNS)
    seen = set(columns)
    needs_match = False
    for cp in compiled:
        if cp.group_columns:
            pattern_columns = [column for _group, column in cp.group_columns]
        elif cp.match_column == MATCH_COLUMN:
            needs_match = True
            pattern_columns = []
        else:
            pattern_columns = [cp.match_column]
        for column in pattern_columns:
            if column not in seen:
                seen.add(column)
                columns.append(column)
    if needs_match:
        columns.append(MATCH_COLUMN)
    return columns


@lru_cache(maxsize=8)
def _compile_cached(patterns: tuple[PatternDef, ...]) -> tuple[CompiledPattern, ...]:
    """Per-process cache so worker processes compile each pattern set once."""
    return tuple(compile_patterns(patterns))


# ---------------------------------------------------------------------------
# File discovery
# ---------------------------------------------------------------------------

def collect_files(folder: Path, file_patterns: Iterable[str]) -> list[Path]:
    """
    Resolve glob patterns relative to ``folder`` (``*.log``, ``**/*.txt`` ...).
    Without patterns every file in the folder is used (also files without an
    extension). Returns a stable, sorted list.
    """
    folder = Path(folder)
    if not folder.is_dir():
        raise ValueError(f"Target folder does not exist: {folder}")

    patterns = [p.strip() for p in file_patterns if p and p.strip()] or ["*"]
    found: set[Path] = set()
    for pattern in patterns:
        try:
            candidates = list(folder.glob(pattern))
        except (ValueError, NotImplementedError) as exc:
            raise ValueError(f"Invalid file pattern '{pattern}': {exc}") from exc
        for candidate in candidates:
            try:
                if candidate.is_file():
                    found.add(candidate)
            except OSError:
                continue
    return sorted(found, key=lambda p: str(p).lower())


def file_label(path: Path, folder: Path) -> str:
    """Path relative to the search folder (unique even for ``**`` patterns)."""
    try:
        return path.relative_to(folder).as_posix()
    except ValueError:
        return path.name


# ---------------------------------------------------------------------------
# Reading / decoding
# ---------------------------------------------------------------------------

def detect_encoding(sample: bytes, truncated: bool) -> str | None:
    """
    Return the encoding to read a file with, or ``None`` for binary files.
    Order: BOM → UTF-8 (strict check on the sample) → latin-1 (never fails).
    """
    if sample.startswith(codecs.BOM_UTF8):
        return "utf-8-sig"
    if sample.startswith((codecs.BOM_UTF16_LE, codecs.BOM_UTF16_BE)):
        return "utf-16"
    if b"\x00" in sample:
        return None
    try:
        sample.decode("utf-8")
        return "utf-8"
    except UnicodeDecodeError as exc:
        # A multi-byte character cut in half at the end of the sample is fine.
        if truncated and exc.start >= len(sample) - 3:
            return "utf-8"
        return "latin-1"


def clean_cell(value: Any) -> str:
    """Normalise a captured value: ``None`` → ``""`` and no raw line breaks."""
    if value is None:
        return ""
    return _LINE_BREAKS.sub(" ", value).strip() if "\n" in value or "\r" in value else value


class _LineLocator:
    """
    Converts offsets inside a block into (line, column).  Offsets from one
    ``finditer`` are increasing, so counting is incremental → O(len(block))
    per pattern instead of O(len(block)) per match.
    """

    __slots__ = ("_text", "_first_line", "_pos", "_line", "_line_start")

    def __init__(self, text: str, first_line: int):
        self._text = text
        self._first_line = first_line
        self.reset()

    def reset(self) -> None:
        self._pos = 0
        self._line = self._first_line
        self._line_start = 0

    def locate(self, offset: int) -> tuple[int, int]:
        if offset < self._pos:
            self.reset()
        newlines = self._text.count("\n", self._pos, offset)
        if newlines:
            self._line += newlines
            self._line_start = self._text.rfind("\n", self._pos, offset) + 1
        self._pos = offset
        return self._line, offset - self._line_start + 1


def _search_block(
    text: str,
    start_line: int,
    compiled: Sequence[CompiledPattern],
    label: str,
    rows: list[RowDict],
    limit: int,
) -> bool:
    """Append matches of every pattern in ``text``. Returns True if ``limit`` hit."""
    locator = _LineLocator(text, start_line)
    for cp in compiled:
        locator.reset()
        for match in cp.regex.finditer(text):
            line, column = locator.locate(match.start())
            row: RowDict = {"File": label, "Line": line, "Column": column, "Pattern": cp.name}
            if cp.group_columns:
                groups = match.groupdict()
                for group, column_name in cp.group_columns:
                    row[column_name] = clean_cell(groups.get(group))
            else:
                row[cp.match_column] = clean_cell(match.group(0))
            rows.append(row)
            if limit and len(rows) >= limit:
                return True
    return False


def search_file(
    path: Path,
    compiled: Sequence[CompiledPattern],
    *,
    label: str,
    segmentation_mode: str = "Auto",
    whole_file: bool = False,
    limit: int = 0,
    should_stop: Callable[[], bool] | None = None,
) -> FileResult:
    """Search a single file. Never raises for I/O problems — see ``FileResult.error``."""
    result = FileResult(label)
    try:
        size = path.stat().st_size
        if size == 0:
            return result

        with path.open("rb") as raw:
            sample = raw.read(SNIFF_SIZE)
        encoding = detect_encoding(sample, truncated=size > len(sample))
        if encoding is None:
            result.note = "skipped (binary file)"
            return result

        with path.open("r", encoding=encoding, errors="replace") as handle:
            if whole_file and size <= WHOLE_FILE_MAX_BYTES:
                blocks: Iterable[tuple[int, str]] = [(1, handle.read())]
            else:
                if whole_file:
                    result.note = (
                        f"larger than {WHOLE_FILE_MAX_BYTES // (1024 * 1024)} MB, "
                        "searched in segments instead of as a whole"
                    )
                blocks = iter_blocks(handle, segmentation_mode)

            for start_line, block in blocks:
                if should_stop is not None and should_stop():
                    break
                if _search_block(block, start_line, compiled, label, result.rows, limit):
                    break
    except (OSError, UnicodeError, MemoryError) as exc:
        result.error = f"{type(exc).__name__}: {exc}"
    return result


def _search_file_task(
    path: str,
    label: str,
    patterns: tuple[PatternDef, ...],
    segmentation_mode: str,
    whole_file: bool,
    limit: int,
) -> FileResult:
    """Entry point executed inside a worker process (must stay module level)."""
    return search_file(
        Path(path),
        _compile_cached(patterns),
        label=label,
        segmentation_mode=segmentation_mode,
        whole_file=whole_file,
        limit=limit,
    )


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def _terminate_pool(executor: ProcessPoolExecutor) -> None:
    """Kill worker processes (e.g. stuck in catastrophic regex backtracking)."""
    processes = getattr(executor, "_processes", None) or {}
    for process in list(processes.values()):
        try:
            process.terminate()
        except Exception:
            pass


def run_search(
    options: SearchOptions,
    *,
    on_schema: Callable[[list[str]], None],
    on_rows: Callable[[list[RowDict]], None],
    on_progress: Callable[[int, int], None],
    on_log: Callable[[str], None],
    should_stop: Callable[[], bool],
    workers: int = 1,
    use_processes: bool = True,
) -> SearchSummary:
    """
    Run a complete search. Results are delivered through ``on_rows`` in file
    order (also in parallel mode) so output is deterministic.
    Raises :class:`PatternError` / ``ValueError`` for invalid input.
    """
    started = time.perf_counter()
    summary = SearchSummary()

    compiled = compile_patterns(options.patterns)
    if not compiled:
        raise ValueError("No regex patterns to search with.")
    on_schema(build_schema(compiled))

    on_log("Collecting files...")
    files = collect_files(options.folder, options.file_patterns)
    summary.total_files = len(files)
    if not files:
        on_log("No files found matching the file pattern(s).")
        summary.elapsed = time.perf_counter() - started
        return summary
    on_log(f"Found {len(files)} file(s). Searching with {len(compiled)} pattern(s)...")

    max_rows = max(0, options.max_rows)

    def accept(result: FileResult) -> bool:
        """Deliver one file's result. Returns False once the row limit is hit."""
        summary.searched_files += 1
        if result.error:
            summary.failed_files += 1
            on_log(f"[ERROR] {result.file_label}: {result.error}")
        elif result.note:
            on_log(f"[INFO] {result.file_label}: {result.note}")

        rows = result.rows
        if max_rows:
            remaining = max_rows - summary.total_rows
            if len(rows) >= remaining:
                rows = rows[:remaining]
                summary.limit_reached = True
        if rows:
            summary.total_rows += len(rows)
            on_rows(rows)
        on_progress(summary.searched_files, summary.total_files)
        return not summary.limit_reached

    def remaining_limit() -> int:
        return max_rows - summary.total_rows if max_rows else 0

    if use_processes:
        try:
            _run_in_processes(files, options, workers, accept, remaining_limit, should_stop, summary)
        except BrokenProcessPool as exc:
            if summary.cancelled:
                pass
            else:
                on_log(f"[WARN] Worker processes unavailable ({exc}); continuing in-process.")
                done = summary.searched_files
                _run_in_thread(files[done:], options, compiled, accept, remaining_limit, should_stop, summary)
    else:
        _run_in_thread(files, options, compiled, accept, remaining_limit, should_stop, summary)

    if summary.limit_reached:
        on_log(f"Row limit ({max_rows}) reached — search stopped early.")
    summary.elapsed = time.perf_counter() - started
    return summary


def _run_in_thread(files, options, compiled, accept, remaining_limit, should_stop, summary) -> None:
    for path in files:
        if should_stop():
            summary.cancelled = True
            return
        result = search_file(
            path,
            compiled,
            label=file_label(path, options.folder),
            segmentation_mode=options.segmentation_mode,
            whole_file=options.whole_file,
            limit=remaining_limit(),
            should_stop=should_stop,
        )
        if should_stop():
            summary.cancelled = True
        if not accept(result) or summary.cancelled:
            return


def _run_in_processes(files, options, workers, accept, remaining_limit, should_stop, summary) -> None:
    workers = max(1, min(workers, len(files)))
    window = workers * 2                       # bounded queue → early stop is cheap
    context = multiprocessing.get_context("spawn")   # fork + Qt threads is unsafe
    executor = ProcessPoolExecutor(max_workers=workers, mp_context=context)

    pending: dict[Future, int] = {}
    finished: dict[int, FileResult] = {}
    next_submit = 0
    next_emit = 0
    stop_now = False

    def submit_more() -> None:
        nonlocal next_submit
        while next_submit < len(files) and len(pending) < window:
            path = files[next_submit]
            future = executor.submit(
                _search_file_task,
                str(path),
                file_label(path, options.folder),
                options.patterns,
                options.segmentation_mode,
                options.whole_file,
                remaining_limit(),
            )
            pending[future] = next_submit
            next_submit += 1

    try:
        submit_more()
        while pending and not stop_now:
            done, _ = wait(pending, timeout=0.1, return_when=FIRST_COMPLETED)
            if should_stop():
                summary.cancelled = True
                break
            for future in done:
                index = pending.pop(future)
                path = files[index]
                try:
                    finished[index] = future.result()
                except BrokenProcessPool:
                    raise
                except Exception as exc:          # unexpected error in worker
                    finished[index] = FileResult(
                        file_label(path, options.folder), error=f"{type(exc).__name__}: {exc}"
                    )
            # Emit strictly in file order.
            while next_emit in finished:
                if not accept(finished.pop(next_emit)):
                    stop_now = True
                    break
                next_emit += 1
            if not stop_now:
                submit_more()
    finally:
        aborted = summary.cancelled or stop_now
        if aborted:
            _terminate_pool(executor)
        executor.shutdown(wait=not aborted, cancel_futures=True)
