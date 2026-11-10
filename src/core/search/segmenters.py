r"""
Streaming log segmenters.

A segmenter turns an iterable of text lines into logical *blocks* — the unit a
regex is applied to.  Blocks are yielded as ``(start_line, text)`` tuples where
``start_line`` is the 1-based line number of the block's first line.  The
block's final line break is removed so ``\Z`` / ``$`` anchor at the block end.

Everything streams: only the current block is held in memory, so files of any
size can be searched without loading them completely.
"""
from __future__ import annotations

import itertools
import re
from typing import Iterable, Iterator

Block = tuple[int, str]

SEGMENTATION_MODES = ("Auto", "Timestamp", "Exception", "Line")

# Lines that start a new block in the respective mode. The same patterns are
# used for auto-detection, so detection and segmentation can never disagree.
# Boundaries must start at column 0: indented lines are continuation lines
# (stack frames, wrapped messages), even if they contain a time.
_MONTH = r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)"
TIMESTAMP_BOUNDARY = re.compile(
    r"^\[?(?:"
    r"\d{4}[-/.]\d{2}[-/.]\d{2}"                         # 2024-05-01, 2024/05/01, 2024.05.01 (ISO, incl. ...T12:00)
    r"|\d{2}[-/.]\d{2}[-/.]\d{4}"                        # 01.05.2024, 05/01/2024
    r"|\d{2}/" + _MONTH + r"/\d{4}:\d{2}:\d{2}:\d{2}"    # 01/May/2024:12:00:00 (Apache / NCSA)
    r"|" + _MONTH + r" {1,2}\d{1,2} \d{2}:\d{2}:\d{2}"   # May  1 12:00:00 (syslog)
    r"|\d{1,2}:\d{2}:\d{2}"                              # 12:00:00
    r")"
)
EXCEPTION_BOUNDARY = re.compile(r"^\w+(?:\.\w+)*(?:Exception|Error):")

# Auto-detection only looks at the head of a file.
DETECT_SAMPLE_LINES = 100
# A mode is chosen when the first non-blank line is a boundary, or at least this
# many sample lines are. A single stray match must not switch a plain file into
# block mode — blocks only end at the next boundary, so they could become huge.
DETECT_MIN_BOUNDARIES = 2


def _trim(text: str) -> str:
    """Drop exactly one trailing line break."""
    return text[:-1] if text.endswith("\n") else text


def _looks_segmented(lines: list[str], boundary: re.Pattern) -> bool:
    first = next((line for line in lines if line.strip()), None)
    if first is None:
        return False
    if boundary.match(first):
        return True
    hits = 0
    for line in lines:
        if boundary.match(line):
            hits += 1
            if hits >= DETECT_MIN_BOUNDARIES:
                return True
    return False


def detect_mode(sample: str | list[str]) -> str:
    """Pick the best segmentation mode from the file's first lines (text or list of lines)."""
    lines = sample.splitlines() if isinstance(sample, str) else sample
    if _looks_segmented(lines, TIMESTAMP_BOUNDARY):
        return "Timestamp"
    if _looks_segmented(lines, EXCEPTION_BOUNDARY):
        return "Exception"
    return "Line"


def iter_line_blocks(lines: Iterable[str]) -> Iterator[Block]:
    """Every non-blank line is its own block."""
    for line_no, line in enumerate(lines, start=1):
        if line.strip():
            yield line_no, _trim(line)


def iter_boundary_blocks(lines: Iterable[str], boundary: re.Pattern) -> Iterator[Block]:
    """
    Group lines into blocks; a new block starts at every line matching ``boundary``.
    Continuation lines (stack traces, wrapped messages) stay with their header.
    Whitespace-only blocks are dropped.
    """
    buffer: list[str] = []
    start_line = 1
    for line_no, line in enumerate(lines, start=1):
        if buffer and boundary.match(line):
            text = "".join(buffer)
            if text.strip():
                yield start_line, _trim(text)
            buffer = []
        if not buffer:
            start_line = line_no
        buffer.append(line)

    if buffer:
        text = "".join(buffer)
        if text.strip():
            yield start_line, _trim(text)


def iter_blocks(lines: Iterable[str], mode: str = "Auto") -> Iterator[Block]:
    """Segment ``lines`` according to ``mode`` (one of ``SEGMENTATION_MODES``)."""
    if mode not in SEGMENTATION_MODES:
        mode = "Auto"

    if mode == "Auto":
        lines = iter(lines)
        head = list(itertools.islice(lines, DETECT_SAMPLE_LINES))
        mode = detect_mode(head)
        lines = itertools.chain(head, lines)

    if mode == "Timestamp":
        return iter_boundary_blocks(lines, TIMESTAMP_BOUNDARY)
    if mode == "Exception":
        return iter_boundary_blocks(lines, EXCEPTION_BOUNDARY)
    return iter_line_blocks(lines)
