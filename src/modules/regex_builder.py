import re


class RegexBuilder:
    """
    Helper class for building regex patterns from sample strings.
    """

    def __init__(self, main_window=None):
        self.main_window = main_window

    def build_smart_regex(self, sample: str) -> str:
        """
        Try to detect common patterns and build a regex that generalizes them.
        Returns a regex string, or empty string if input is invalid.
        """
        if not sample:
            return ""  # caller handles empty input

        # --- Common semantic patterns ---
        if re.match(r"^\d{4}-\d{2}-\d{2}$", sample):  # 2025-09-09
            return r"\d{4}-\d{2}-\d{2}"
        if re.match(r"^\d{2}[./-]\d{2}[./-]\d{4}$", sample):  # 09.09.2025 or 09-09-2025
            return r"\d{2}[./-]\d{2}[./-]\d{4}"
        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", sample):  # Email
            return r"[\w\.-]+@[\w\.-]+\.\w+"
        if re.match(r"^(\d{1,3}\.){3}\d{1,3}$", sample):  # IPv4
            return r"(?:\d{1,3}\.){3}\d{1,3}"
        if re.match(r"^[0-9a-fA-F-]{36}$", sample):  # UUID
            return r"[0-9a-fA-F-]{36}"
        if re.match(r"^[0-9a-fA-F]+$", sample):  # Hex string
            return r"[0-9a-fA-F]+"
        if re.match(r"^\+?\d[\d\s-]{7,}$", sample):  # Phone number
            return r"\+?\d[\d\s-]{7,}"

        # --- Fallback: rule-based generation ---
        regex_parts = []
        i = 0
        while i < len(sample):
            char = sample[i]
            if char.isdigit():
                j = i
                while j < len(sample) and sample[j].isdigit():
                    j += 1
                length = j - i
                regex_parts.append(rf"\d{{{length}}}" if length > 1 else r"\d")
                i = j
                continue
            elif char.isalpha():
                j = i
                while j < len(sample) and sample[j].isalpha():
                    j += 1
                length = j - i
                regex_parts.append(rf"[A-Za-z]{{{length}}}" if length > 1 else r"[A-Za-z]")
                i = j
                continue
            elif char.isspace():
                regex_parts.append(r"\s+")
            else:
                regex_parts.append(re.escape(char))
            i += 1
            
        return "".join(regex_parts)

