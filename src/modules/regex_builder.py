import re
from typing import Optional, List, Tuple

class RegexBuilder:
    """
    Enhanced helper class for building regex patterns with named groups from sample strings.
    """
    
    def __init__(self, main_window=None):
        self.main_window = main_window
        self.common_patterns = {
            'ip': {
                'match_pattern': r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",
                'regex_pattern': r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}",
                'grouped_pattern': r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
            },
            'email': {
                'match_pattern': r"^[\w\.-]+@[\w\.-]+\.\w+$",
                'regex_pattern': r"[\w\.-]+@[\w\.-]+\.\w+",
                'grouped_pattern': r"(?P<email>[\w\.-]+@[\w\.-]+\.\w+)"
            },
            'date_iso': {
                'match_pattern': r"^\d{4}-\d{2}-\d{2}$",
                'regex_pattern': r"\d{4}-\d{2}-\d{2}",
                'grouped_pattern': r"(?P<date>\d{4}-\d{2}-\d{2})"
            },
            'date_us': {
                'match_pattern': r"^\d{2}[./-]\d{2}[./-]\d{4}$",
                'regex_pattern': r"\d{2}[./-]\d{2}[./-]\d{4}",
                'grouped_pattern': r"(?P<date>\d{2}[./-]\d{2}[./-]\d{4})"
            },
            'time': {
                'match_pattern': r"^\d{1,2}:\d{2}(:\d{2})?$",
                'regex_pattern': r"\d{1,2}:\d{2}(?::\d{2})?",
                'grouped_pattern': r"(?P<time>\d{1,2}:\d{2}(?::\d{2})?)"
            },
            'datetime': {
                'match_pattern': r"^\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}$",
                'regex_pattern': r"\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}",
                'grouped_pattern': r"(?P<datetime>\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2})"
            },
            'uuid': {
                'match_pattern': r"^[0-9a-fA-F-]{36}$",
                'regex_pattern': r"[0-9a-fA-F-]{36}",
                'grouped_pattern': r"(?P<uuid>[0-9a-fA-F-]{36})"
            },
            'hex': {
                'match_pattern': r"^[0-9a-fA-F]+$",
                'regex_pattern': r"[0-9a-fA-F]+",
                'grouped_pattern': r"(?P<hex>[0-9a-fA-F]+)"
            },
            'phone': {
                'match_pattern': r"^\+?\d[\d\s-]{7,}$",
                'regex_pattern': r"\+?\d[\d\s-]{7,}",
                'grouped_pattern': r"(?P<phone>\+?\d[\d\s-]{7,})"
            },
            'url': {
                'match_pattern': r"^https?://[^\s]+$",
                'regex_pattern': r"https?://[^\s]+",
                'grouped_pattern': r"(?P<url>https?://[^\s]+)"
            },
            'number': {
                'match_pattern': r"^\d+$",
                'regex_pattern': r"\d+",
                'grouped_pattern': r"(?P<number>\d+)"
            },
            'decimal': {
                'match_pattern': r"^\d+\.\d+$",
                'regex_pattern': r"\d+\.\d+",
                'grouped_pattern': r"(?P<decimal>\d+\.\d+)"
            },
            'word': {
                'match_pattern': r"^[A-Za-z]+$",
                'regex_pattern': r"[A-Za-z]+",
                'grouped_pattern': r"(?P<word>[A-Za-z]+)"
            },
            'http_method': {
                'match_pattern': r"^(GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH)$",
                'regex_pattern': r"(?:GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH)",
                'grouped_pattern': r"(?P<method>GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH)"
            },
            'http_status': {
                'match_pattern': r"^[1-5]\d{2}$",
                'regex_pattern': r"[1-5]\d{2}",
                'grouped_pattern': r"(?P<status>[1-5]\d{2})"
            },
        }
    
    def detect_pattern_type(self, sample: str) -> Optional[str]:
        """Detect what type of pattern the sample represents."""
        sample = sample.strip()
        for pattern_name, pattern_info in self.common_patterns.items():
            if re.match(pattern_info['match_pattern'], sample):
                return pattern_name
        return None
    
    def build_smart_regex(self, sample: str, group_name: str = None, use_groups: bool = False) -> str:
        """
        Build a regex pattern from a sample string, optionally with named groups.
        This is your existing method signature, enhanced with grouping capability.
        """
        if not sample:
            return ""
        
        sample = sample.strip()
        
        # Check for common semantic patterns first
        pattern_type = self.detect_pattern_type(sample)
        if pattern_type:
            pattern_info = self.common_patterns[pattern_type]
            
            if use_groups:
                if group_name:
                    # Use custom group name
                    return pattern_info['regex_pattern'].replace(
                        pattern_info['regex_pattern'],
                        f"(?P<{group_name}>{pattern_info['regex_pattern']})"
                    )
                else:
                    # Use default grouped pattern
                    return pattern_info['grouped_pattern']
            else:
                # Return ungrouped version
                return pattern_info['regex_pattern']
        
        # Fallback: rule-based generation (your existing logic)
        return self._build_fallback_regex(sample, group_name, use_groups)
    
    def _build_fallback_regex(self, sample: str, group_name: str = None, use_groups: bool = False) -> str:
        """Build regex using character-by-character analysis (your existing logic enhanced)."""
        regex_parts = []
        i = 0
        
        while i < len(sample):
            char = sample[i]
            
            if char.isdigit():
                j = i
                while j < len(sample) and sample[j].isdigit():
                    j += 1
                length = j - i
                pattern = rf"\d{{{length}}}" if length > 1 else r"\d"
                regex_parts.append(pattern)
                i = j
                
            elif char.isalpha():
                j = i
                while j < len(sample) and sample[j].isalpha():
                    j += 1
                length = j - i
                pattern = rf"[A-Za-z]{{{length}}}" if length > 1 else r"[A-Za-z]"
                regex_parts.append(pattern)
                i = j
                
            elif char.isspace():
                # Count consecutive spaces
                j = i
                while j < len(sample) and sample[j].isspace():
                    j += 1
                regex_parts.append(r"\s+" if j - i > 1 else r"\s")
                i = j
                
            else:
                regex_parts.append(re.escape(char))
                i += 1
        
        pattern = "".join(regex_parts)
        
        if use_groups and group_name:
            pattern = f"(?P<{group_name}>{pattern})"
        
        return pattern
    
    def build_complex_regex_with_groups(self, samples_and_groups: List[Tuple[str, str]]) -> str:
        """
        Build a complex regex from multiple samples with their group names.
        samples_and_groups: List of (sample_text, group_name) tuples
        
        Example:
        samples = [
            ("192.168.1.1", "ip"),
            ("GET", "method"), 
            ("/index.html", "path")
        ]
        Returns: r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(?P<method>GET)(?P<path>/index\.html)"
        """
        if not samples_and_groups:
            return ""
        
        patterns = []
        for sample_text, group_name in samples_and_groups:
            if sample_text.strip() and group_name.strip():
                pattern = self.build_smart_regex(sample_text.strip(), group_name.strip(), use_groups=True)
                if pattern:
                    patterns.append(pattern)
        
        return "".join(patterns)
    
    def extract_groups_from_regex(self, regex_pattern: str) -> List[str]:
        """Extract all named group names from a regex pattern."""
        group_pattern = r'\(\?P<(\w+)>'
        return re.findall(group_pattern, regex_pattern)
    
    def suggest_group_names_from_sample(self, sample: str) -> List[str]:
        """Suggest potential group names based on the sample content."""
        suggestions = []
        
        # Check against known patterns
        pattern_type = self.detect_pattern_type(sample)
        if pattern_type:
            # Extract the default group name from grouped pattern
            grouped_pattern = self.common_patterns[pattern_type]['grouped_pattern']
            groups = self.extract_groups_from_regex(grouped_pattern)
            suggestions.extend(groups)
        
        # Add generic suggestions based on content
        sample_lower = sample.lower().strip()
        
        if any(word in sample_lower for word in ['error', 'err', 'exception']):
            suggestions.append('error')
        if any(word in sample_lower for word in ['user', 'username', 'login']):
            suggestions.append('user')
        if any(word in sample_lower for word in ['id', 'identifier']):
            suggestions.append('id')
        if any(word in sample_lower for word in ['name', 'title']):
            suggestions.append('name')
        if any(word in sample_lower for word in ['path', 'file', 'url']):
            suggestions.append('path')
        if any(word in sample_lower for word in ['size', 'length', 'bytes']):
            suggestions.append('size')
        
        return list(dict.fromkeys(suggestions))  # Remove duplicates while preserving order
    
    def validate_regex_pattern(self, pattern: str) -> Tuple[bool, str]:
        """
        Validate a regex pattern and return (is_valid, error_message).
        """
        try:
            re.compile(pattern)
            return True, ""
        except re.error as e:
            return False, str(e)
    
    def get_pattern_info(self, sample: str) -> dict:
        """
        Get comprehensive information about a sample string and its potential regex patterns.
        """
        pattern_type = self.detect_pattern_type(sample)
        suggestions = self.suggest_group_names_from_sample(sample)
        
        info = {
            'sample': sample,
            'detected_type': pattern_type,
            'suggested_groups': suggestions,
            'basic_regex': self.build_smart_regex(sample, use_groups=False),
            'grouped_regex': self.build_smart_regex(sample, use_groups=True) if pattern_type else None,
        }
        
        return info