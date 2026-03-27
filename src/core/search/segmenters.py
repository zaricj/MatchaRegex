import re
from typing import List


class BaseSegmenter:
    def split(self, text: str) -> List[str]:
        raise NotImplementedError


class TimestampSegmenter(BaseSegmenter):
    """
    Splits a log file into multi-line blocks, where each block starts
    with a timestamp. Handles log entries that span multiple lines.
    e.g.:
        12:00:01 Starting process
        12:00:02 Error occurred
                 details on second line   <- kept with the block above
        12:00:03 Done
    """
    def __init__(self, pattern: str = r'\d{2}:\d{2}:\d{2}'):
        # Use a lookahead so the timestamp itself is kept at the start of each block
        self.regex = re.compile(rf'(?=^\s*{pattern})', re.MULTILINE)

    def split(self, text: str) -> List[str]:
        return [b for b in self.regex.split(text) if b.strip()]


class ExceptionSegmenter(BaseSegmenter):
    """
    Splits on Java/Python-style exception boundaries.
    e.g. "com.example.SomeException:" or "ValueError:"
    Keeps the exception header attached to its stack trace.
    """
    def split(self, text: str) -> List[str]:
        blocks = re.split(
            r'(?=^\w+(?:\.\w+)*(?:Exception|Error):)',
            text,
            flags=re.MULTILINE
        )
        return [b for b in blocks if b.strip()]


class LineSegmenter(BaseSegmenter):
    """
    Fallback: each line is its own block. Used for simple single-line log formats.
    """
    def split(self, text: str) -> List[str]:
        return [line for line in text.splitlines() if line.strip()]


def detect_segmenter(text: str) -> BaseSegmenter:
    """
    Inspects the first ~50 lines to decide the best segmenter.
    Avoids scanning the entire file just for detection.
    """
    sample = "\n".join(text.splitlines()[:50])

    if re.search(r'^\d{2}:\d{2}:\d{2}', sample, re.MULTILINE):
        return TimestampSegmenter()  # uses default pattern, don't pass text

    if re.search(r'^\w+(?:\.\w+)*(?:Exception|Error):', sample, re.MULTILINE):
        return ExceptionSegmenter()

    return LineSegmenter()