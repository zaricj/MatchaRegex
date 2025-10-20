from collections import Counter, defaultdict
from typing import Any

def count_occurrences_by_key(results: list[dict[str, Any]], key_field: str) -> list[dict[str, Any]]:
    """
    Count how many times each unique value of `key_field` occurs per file.
    Returns a summarized list of dicts like:
        [{"File": "file1.log", "user": "alice", "Count": 3}, ...]
    """
    if not results or key_field not in results[0]:
        return []

    counts = defaultdict(Counter)
    for r in results:
        file = r.get("File", "")
        key_value = r.get(key_field, "")
        if key_value:
            counts[file][key_value] += 1

    summary = []
    for file, file_counts in counts.items():
        for value, count in file_counts.items():
            summary.append({"File": file, key_field: value, "Count": count})
    return summary
