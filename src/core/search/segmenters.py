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

# Lines that start a new block in the respective mode.
TIMESTAMP_BOUNDARY = re.compile(r"^\s*\d{2}:\d{2}:\d{2}")
EXCEPTION_BOUNDARY = re.compile(r"^\w+(?:\.\w+)*(?:Exception|Error):")

# Auto-detection only looks at the head of a file.
DETECT_SAMPLE_LINES = 100
_DETECT_TIMESTAMP = re.compile(r"^\d{2}:\d{2}:\d{2}", re.MULTILINE)
_DETECT_EXCEPTION = re.compile(r"^\w+(?:\.\w+)*(?:Exception|Error):", re.MULTILINE)


def _trim(text: str) -> str:
    """Drop exactly one trailing line break."""
    return text[:-1] if text.endswith("\n") else text


def detect_mode(sample: str) -> str:
    """Pick the best segmentation mode from a sample of the file's first lines."""
    if _DETECT_TIMESTAMP.search(sample):
        return "Timestamp"
    if _DETECT_EXCEPTION.search(sample):
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
        mode = detect_mode("".join(head))
        lines = itertools.chain(head, lines)

    if mode == "Timestamp":
        return iter_boundary_blocks(lines, TIMESTAMP_BOUNDARY)
    if mode == "Exception":
        return iter_boundary_blocks(lines, EXCEPTION_BOUNDARY)
    return iter_line_blocks(lines)
