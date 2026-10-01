import re
from typing import List, Tuple


class BaseSegmenter:
    def split(self, text: str) -> List[Tuple[int, str]]:
        """Returns a list of (start_offset, text_block) tuples."""
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

    def split(self, text: str) -> List[Tuple[int, str]]:
        matches = list(self.regex.finditer(text))
        if not matches:
            return [(0, text)] if text.strip() else []

        blocks = []
        # First block: from 0 to first match start
        if matches[0].start() > 0:
            content = text[:matches[0].start()]
            if content.strip():
                blocks.append((0, content))
            else:
                # If it's just whitespace, we treat it as the start of the first block
                # but we need to handle the fact that the first segment is empty.
                # Actually, let's just add it and let the consumer handle it.
                blocks.append((0, content))
        else:
            # The first match starts at 0
            pass

        # Intermediate blocks
        for i in range(len(matches) - 1):
            start = matches[i].start()
            end = matches[i+1].start()
            content = text[start:end]
            if content.strip():
                blocks.append((start, content))
            elif i == 0 and matches[0].start() == 0:
                # If the first match was at 0, we already handled the 'start'
                pass
            else:
                # Handle empty blocks if they aren't just whitespace
                blocks.append((start, content))

        # Last block: from last match start to end of text
        last_start = matches[-1].start()
        last_content = text[last_start:]
        if last_content.strip():
            blocks.append((last_start, last_content))
        elif last_start < len(text):
            # It might be whitespace, but still worth including if it's not just empty
            blocks.append((last_start, last_content))

        # Filter out truly empty/whitespace blocks that aren't needed
        # but we should be careful not to break the offsets.
        # Actually, it's safer to return all blocks and let the consumer filter.
        # But to match previous behavior:
        
        # Let's re-do it more carefully.
        return self._get_segments(text, matches)

    def _get_segments(self, text: str, matches: list) -> List[Tuple[int, str]]:
        segments = []
        last_pos = 0
        for m in matches:
            start = m.start()
            if start > last_pos:
                content = text[last_pos:start]
                if content.strip():
                    segments.append((last_pos, content))
            last_pos = start
        
        # Last segment
        if last_pos < len(text):
            content = text[last_pos:]
            if content.strip():
                segments.append((last_pos, content))
        
        # If no segments found but text is not empty
        if not segments and text.strip():
            segments.append((0, text))
            
        return segments


class ExceptionSegmenter(BaseSegmenter):
    """
    Splits on Java/Python-style exception boundaries.
    e.g. "com.example.SomeException:" or "ValueError:"
    Keeps the exception header attached to its stack trace.
    """
    def split(self, text: str) -> List[Tuple[int, str]]:
        # pattern: r'(?=^\w+(?:\.\w+)*(?:Exception|Error):)'
        pattern = r'(?=^\w+(?:\.\w+)*(?:Exception|Error):)'
        matches = list(re.finditer(pattern, text, flags=re.MULTILINE))
        return self._get_segments(text, matches)

    def _get_segments(self, text: str, matches: list) -> List[Tuple[int, str]]:
        segments = []
        last_pos = 0
        for m in matches:
            start = m.start()
            if start > last_pos:
                content = text[last_pos:start]
                if content.strip():
                    segments.append((last_pos, content))
            last_pos = start
        
        if last_pos < len(text):
            content = text[last_pos:]
            if content.strip():
                segments.append((last_pos, content))
        
        if not segments and text.strip():
            segments.append((0, text))
            
        return segments


class LineSegmenter(BaseSegmenter):
    """
    Fallback: each line is its own block. Used for simple single-line log formats.
    """
    def split(self, text: str) -> List[Tuple[int, str]]:
        segments = []
        for m in re.finditer(r'\n', text):
            # The newline is at m.start()
            # The line is from the last newline (or 0) to m.start()
            # But we want to include the newline.
            pass
        # Simpler:
        # Just iterate through lines and their offsets.
        
        lines = text.splitlines(keepends=True)
        current_offset = 0
        for line in lines:
            if line.strip():
                segments.append((current_offset, line))
            current_offset += len(line)
        
        return segments

def detect_segmenter(text: str) -> BaseSegmenter:
    """
    Inspects the first ~100 lines to decide the best segmenter.
    Avoids scanning the entire file just for detection.
    """
    sample = "\n".join(text.splitlines()[:100])

    if re.search(r'^\d{2}:\d{2}:\d{2}', sample, re.MULTILINE):
        return TimestampSegmenter()

    if re.search(r'^\w+(?:\.\w+)*(?:Exception|Error):', sample, re.MULTILINE):
        return ExceptionSegmenter()

    return LineSegmenter()
