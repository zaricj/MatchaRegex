from __future__ import annotations

import json
import os
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any, Sequence

from PySide6.QtWidgets import QMessageBox, QWidget

KeyPath = str | Sequence[str]


class ConfigHandler:
    """
    JSON configuration store.

    * One instance should be shared by the whole application (the main window
      owns it) so different windows never overwrite each other's changes.
    * Values are cached in memory; every change is written atomically
      (temp file + ``os.replace``) so a crash can never leave a half written file.
    * A corrupt file is backed up instead of silently wiped.
    * Key paths are either dot strings (``"a.b.c"``) or sequences
      (``["a", "name.with.dots", "c"]``) — use sequences for user supplied names.
    """

    def __init__(self, config_directory: Path, config_file_name: Path, main_window: QWidget | None = None):
        self.config_directory = Path(config_directory)
        self.config_file_name = Path(config_file_name)
        self.main_window = main_window
        self.config_directory.mkdir(parents=True, exist_ok=True)
        self.data: dict = self._load_config()

    # ----- persistence -----

    def _load_config(self) -> dict:
        if not self.config_file_name.exists():
            return {}
        try:
            with open(self.config_file_name, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            if isinstance(data, dict):
                return data
            raise ValueError("top level JSON value is not an object")
        except (json.JSONDecodeError, ValueError, UnicodeDecodeError) as exc:
            backup = self.config_file_name.with_name(
                f"{self.config_file_name.stem}.corrupt-{time.strftime('%Y%m%d-%H%M%S')}.json"
            )
            try:
                shutil.copy2(self.config_file_name, backup)
                where = f"A backup was saved as:\n{backup}"
            except OSError:
                where = "A backup could not be created."
            QMessageBox.warning(
                self.main_window,
                "Load config warning",
                f"{self.config_file_name} contains invalid JSON ({exc}).\n"
                f"Starting with an empty configuration. {where}",
            )
            return {}
        except OSError as exc:
            QMessageBox.warning(self.main_window, "Load config warning", f"Could not read configuration: {exc}")
            return {}

    def save_config(self) -> None:
        self.config_directory.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=self.config_directory, prefix=".config-", suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(self.data, handle, indent=4, ensure_ascii=False)
            os.replace(tmp, self.config_file_name)
        except BaseException:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise

    # ----- key helpers -----

    @staticmethod
    def _keys(key_path: KeyPath) -> list[str]:
        if isinstance(key_path, str):
            return [k for k in key_path.split(".") if k]
        return [str(k) for k in key_path]

    # ----- public API -----

    def get(self, key_path: KeyPath, default: Any = None) -> Any:
        current: Any = self.data
        for key in self._keys(key_path):
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return default
        return current

    def set(self, key_path: KeyPath, value: Any) -> None:
        keys = self._keys(key_path)
        if not keys:
            raise ValueError("Empty configuration key path")
        parent = self.data
        for key in keys[:-1]:
            if not isinstance(parent.get(key), dict):
                parent[key] = {}
            parent = parent[key]
        parent[keys[-1]] = value
        self.save_config()

    def delete(self, key_path: KeyPath) -> bool:
        keys = self._keys(key_path)
        if not keys:
            return False
        parent: Any = self.data
        for key in keys[:-1]:
            parent = parent.get(key) if isinstance(parent, dict) else None
            if not isinstance(parent, dict):
                return False
        if keys[-1] in parent:
            del parent[keys[-1]]
            self.save_config()
            return True
        return False

    def reset_config(self) -> None:
        self.data = {}
        self.save_config()

    def reload(self) -> None:
        self.data = self._load_config()

    def get_all_keys(self, key_path: KeyPath | None = None) -> list[str]:
        if key_path:
            nested = self.get(key_path, {})
            return list(nested.keys()) if isinstance(nested, dict) else []
        return list(self.data.keys())
