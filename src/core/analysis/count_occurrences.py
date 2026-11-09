from collections import Counter
from typing import Any, Iterable


def count_occurrences_by_key(results: Iterable[dict[str, Any]], key_field: str) -> tuple[list[str], list[dict[str, Any]]]:
    """
    Count how many times each non-empty value of ``key_field`` occurs per file.

    Returns ``(columns, rows)`` sorted by file, then by count (descending), e.g.
    ``(["File", "user", "Count"], [{"File": "a.log", "user": "alice", "Count": 3}, ...])``.
    """
    counts: Counter[tuple[str, Any]] = Counter()
    for row in results:
        value = row.get(key_field, "")
        if value not in ("", None):
            counts[(row.get("File", ""), value)] += 1

    if key_field == "File":
        columns = ["File", "Count"]
        summary = [{"File": f, "Count": c} for (f, _v), c in counts.items()]
    else:
        columns = ["File", key_field, "Count"]
        summary = [{"File": f, key_field: v, "Count": c} for (f, v), c in counts.items()]

    summary.sort(key=lambda r: (str(r["File"]).lower(), -r["Count"]))
    return columns, summary
