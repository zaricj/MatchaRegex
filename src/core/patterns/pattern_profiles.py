from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class PatternSpec:
    """
    A named regex pattern specification.

    ``name``       — human-readable identifier (used for logging / UI display,
                     *not* written as a DataFrame column header).
    ``expression`` — the raw regex string; named capture groups (``(?P<col>…)``)
                     become the DataFrame / CSV column headers.
    """
    name: str
    expression: str

    def group_names(self) -> list[str]:
        """Return the list of named groups declared in ``expression``, in order."""
        return list(re.compile(self.expression).groupindex.keys())


class PatternProfileService:
    """Loads named regex profiles from JSON files."""

    def __init__(self, config_path: Path):
        self.config_path = Path(config_path)

    def load(self) -> dict:
        with self.config_path.open("r", encoding="utf-8") as handle:
            return json.load(handle)

    def list_profiles(self) -> list[str]:
        payload  = self.load()
        profiles = payload.get("profiles")
        if isinstance(profiles, dict) and profiles:
            return sorted(str(key) for key in profiles.keys())
        return ["default"]

    def get_profile_patterns(self, profile_name: str | None = None) -> list[PatternSpec]:
        payload  = self.load()
        profiles = payload.get("profiles")

        if not isinstance(profiles, dict) or not profiles:
            return self._extract_pattern_specs(payload)

        selected_profile = (profile_name or "").strip()
        if not selected_profile:
            selected_profile = str(payload.get("default_profile", "")).strip()
        if not selected_profile:
            selected_profile = sorted(profiles.keys())[0]

        base_patterns    = payload.get("base_patterns")
        profile_patterns = profiles.get(selected_profile, {})
        merged           = self._merge_pattern_config(base_patterns, profile_patterns)
        return self._extract_pattern_specs(merged)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _merge_pattern_config(
        self,
        base_patterns_obj: object,
        selected_patterns: object,
    ) -> dict:
        if not isinstance(base_patterns_obj, dict):
            return dict(selected_patterns) if isinstance(selected_patterns, dict) else {}

        merged = dict(base_patterns_obj)
        if not isinstance(selected_patterns, dict):
            return merged

        for key, value in selected_patterns.items():
            if (
                key in merged
                and isinstance(merged[key], dict)
                and isinstance(value, dict)
            ):
                nested = dict(merged[key])
                nested.update(value)
                merged[key] = nested
            else:
                merged[key] = value

        return merged

    def _extract_pattern_specs(
        self,
        payload: dict,
        parent_key: str = "",
    ) -> list[PatternSpec]:
        """
        Walk the config dict recursively and collect ``PatternSpec`` objects.

        Rules:
        - Only leaf values whose key contains "pattern" (case-insensitive) are
          treated as regex strings.
        - The dotted config path becomes the spec ``name`` (e.g. ``http.url_pattern``
          → ``http_url_pattern``).  This name is purely for identification; CSV
          column headers come from regex named groups, not from this label.
        - Empty or non-string values are skipped.
        """
        results: list[PatternSpec] = []

        for key, value in payload.items():
            current_key = f"{parent_key}.{key}" if parent_key else str(key)

            if isinstance(value, dict):
                results.extend(self._extract_pattern_specs(value, current_key))
                continue

            if not isinstance(value, str):
                continue

            pattern_text = value.strip()
            if not pattern_text:
                continue

            if "pattern" not in key.lower():
                continue

            label = current_key.replace(".", "_")
            results.append(PatternSpec(name=label, expression=pattern_text))

        return results