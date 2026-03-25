import re
import mmap
import pandas as pd
from typing import Any
from pathlib import Path
from PySide6.QtCore import QObject, Signal
from core.patterns.pattern_profiles import PatternSpec


class RegexProcessorSignals(QObject):
    message_information = Signal(str, str)
    message_warning = Signal(str, str)
    message_critical = Signal(str, str)
    program_output_text = Signal(str)
    statusbar_show_message = Signal(str, int)
    progress_update = Signal(int)
    finished = Signal(pd.DataFrame)


class RegexSearchTask:
    def __init__(self, regex_patterns: list = None, folder_path: Path = None,
                 file_patterns: list[str] = None, multiline: bool = False, max_rows: int = 0,
                 signals: RegexProcessorSignals | None = None):
        self.signals = signals or RegexProcessorSignals()
        self.regex_patterns = regex_patterns if regex_patterns is not None else []
        self.folder_path = folder_path
        self.file_patterns = file_patterns if file_patterns is not None else []
        self.multiline = multiline
        self.max_rows = max_rows

    def _normalize_pattern_specs(self) -> list[PatternSpec]:
        normalized: list[PatternSpec] = []
        for index, pattern in enumerate(self.regex_patterns, start=1):
            if isinstance(pattern, PatternSpec):
                normalized.append(pattern)
            elif isinstance(pattern, dict):
                expression = str(pattern.get("expression", "")).strip()
                if expression:
                    normalized.append(
                        PatternSpec(
                            name=str(pattern.get("name", f"Pattern{index}")).strip() or f"Pattern{index}",
                            expression=expression,
                        )
                    )
            else:
                expression = str(pattern).strip()
                if expression:
                    normalized.append(
                        PatternSpec(name=f"Pattern{index}", expression=expression)
                    )
        return normalized

    def process_single_file_universal(self, filepath: Path, compiled_patterns):
        """
        Memory-mapped byte search. 
        Handles 10GB+ files by only reading small slices into RAM.
        """
        results = []
        try:
            file_size = filepath.stat().st_size
            if file_size == 0:
                return []

            with open(filepath, "rb") as f:
                # mmap is the key to 10GB+ files without crashing
                with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                    for pattern_spec, compiled_regex in compiled_patterns:
                        # finditer on mmap is extremely memory efficient
                        for match in compiled_regex.finditer(mm):
                            row = {
                                "File": filepath.name,
                                "Pattern": pattern_spec.name
                            }
                            
                            groupdict = match.groupdict()
                            if groupdict:
                                # FIX: In Python re, groupdict KEYS are already 'str'
                                # only the VALUES are 'bytes' when searching bytes.
                                for key, val_bytes in groupdict.items():
                                    if val_bytes is not None:
                                        # Use latin-1 to handle special chars (like 'März') safely
                                        row[key] = val_bytes.decode('latin-1', 'replace')
                                    else:
                                        row[key] = ""
                            else:
                                # Fallback if no named groups (?P<...>) are used
                                match_bytes = match.group(0)
                                row["Match"] = match_bytes.decode('latin-1', 'replace')

                            results.append(row)

                            # Early exit if we hit the limit for this file
                            if 0 < self.max_rows <= len(results):
                                return results
            return results
        except Exception as ex:
            # We emit a warning instead of crashing so other files can still be processed
            self.signals.message_warning.emit("Search Error", f"Could not process {filepath.name}: {str(ex)}")
            return []

    def search_files(self) -> list[dict[str, Any]]:
        # 1. Gather Files
        if not self.folder_path or not self.folder_path.exists():
            raise ValueError("Target folder does not exist.")

        files = []
        if self.file_patterns and any(fp.strip() for fp in self.file_patterns):
            valid_patterns = [fp.strip() for fp in self.file_patterns if fp.strip()]
            file_set = set()
            for p in valid_patterns:
                file_set.update(self.folder_path.glob(p))
            files = sorted(list(file_set), key=lambda x: x.name)
        else:
            files = sorted(list(self.folder_path.glob('*.*')), key=lambda x: x.name)

        if not files:
            self.signals.program_output_text.emit("No files found matching patterns.")
            return []

        # 2. Compile Patterns as BYTES
        # MULTILINE is necessary for ^ to work on every line of a 10GB file
        flags = re.MULTILINE
        if self.multiline:
            flags |= re.DOTALL

        compiled_list = []
        for spec in self._normalize_pattern_specs():
            try:
                # Convert string pattern to bytes so it can search the mmap buffer
                byte_expr = spec.expression.encode('utf-8')
                compiled_list.append((spec, re.compile(byte_expr, flags)))
            except re.error as e:
                raise ValueError(f"Regex Error in '{spec.name}': {e}")

        # 3. Process
        all_results = []
        total = len(files)
        for index, filepath in enumerate(files, start=1):
            if not filepath.is_file(): continue
            
            self.signals.program_output_text.emit(f"Scanning: {filepath.name}")
            
            file_matches = self.process_single_file_universal(filepath, compiled_list)
            all_results.extend(file_matches)
            
            self.signals.progress_update.emit(int((index / total) * 100))
            
            if 0 < self.max_rows <= len(all_results):
                self.signals.program_output_text.emit(f"Row limit ({self.max_rows}) reached.")
                break
                
        return all_results

    def run(self):
        try:
            self.signals.program_output_text.emit("Starting Search...")
            results = self.search_files()

            if results:
                self.signals.program_output_text.emit(f"Formatting {len(results)} matches...")
                
                # Create DataFrame
                df = pd.DataFrame(results)
                
                # Fill gaps if different regexes have different group names
                df = df.fillna("").astype(str)
                
                # Put core columns at the start
                cols = df.columns.tolist()
                head = [c for c in ["File", "Pattern"] if c in cols]
                body = sorted([c for c in cols if c not in head])
                df = df[head + body]

                self.signals.finished.emit(df)
            else:
                self.signals.program_output_text.emit("Search finished with 0 results.")
                self.signals.finished.emit(pd.DataFrame())

        except Exception as e:
            self.signals.message_critical.emit("Fatal Search Error", str(e))
            self.signals.finished.emit(pd.DataFrame())


def run_regex_search(regex_patterns: list = None, folder_path: Path = None,
                     file_patterns: list[str] | None = None, multiline: bool = False,
                     max_rows: int = 0, signals: RegexProcessorSignals | None = None):
    task = RegexSearchTask(
        regex_patterns=regex_patterns,
        folder_path=folder_path,
        file_patterns=file_patterns,
        multiline=multiline,
        max_rows=max_rows,
        signals=signals,
    )
    task.run()