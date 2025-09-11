import re
import csv
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                              QWidget, QPushButton, QLineEdit, QListWidget, QTextEdit,
                              QLabel, QFileDialog, QProgressBar, QCheckBox, QComboBox,
                              QMessageBox, QSplitter, QGroupBox, QListWidgetItem)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QFont

class RegexBuilder:
    """
    Enhanced helper class for building regex patterns with named groups from sample strings.
    """
    
    def __init__(self, main_window=None):
        self.main_window = main_window
        self.common_patterns = {
            'ip': (r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"),
            'email': (r"^[\w\.-]+@[\w\.-]+\.\w+$", r"(?P<email>[\w\.-]+@[\w\.-]+\.\w+)"),
            'date_iso': (r"^\d{4}-\d{2}-\d{2}$", r"(?P<date>\d{4}-\d{2}-\d{2})"),
            'date_us': (r"^\d{2}[./-]\d{2}[./-]\d{4}$", r"(?P<date>\d{2}[./-]\d{2}[./-]\d{4})"),
            'time': (r"^\d{1,2}:\d{2}(:\d{2})?$", r"(?P<time>\d{1,2}:\d{2}(?::\d{2})?)"),
            'uuid': (r"^[0-9a-fA-F-]{36}$", r"(?P<uuid>[0-9a-fA-F-]{36})"),
            'hex': (r"^[0-9a-fA-F]+$", r"(?P<hex>[0-9a-fA-F]+)"),
            'phone': (r"^\+?\d[\d\s-]{7,}$", r"(?P<phone>\+?\d[\d\s-]{7,})"),
            'url': (r"^https?://[^\s]+$", r"(?P<url>https?://[^\s]+)"),
            'number': (r"^\d+$", r"(?P<number>\d+)"),
            'decimal': (r"^\d+\.\d+$", r"(?P<decimal>\d+\.\d+)"),
            'word': (r"^[A-Za-z]+$", r"(?P<word>[A-Za-z]+)"),
        }
    
    def detect_pattern_type(self, sample: str) -> Optional[str]:
        """Detect what type of pattern the sample represents."""
        for pattern_name, (match_pattern, _) in self.common_patterns.items():
            if re.match(match_pattern, sample.strip()):
                return pattern_name
        return None
    
    def build_smart_regex(self, sample: str, group_name: str = None, use_groups: bool = True) -> str:
        """
        Build a regex pattern from a sample string, optionally with named groups.
        """
        if not sample:
            return ""
        
        sample = sample.strip()
        
        # Check for common semantic patterns first
        pattern_type = self.detect_pattern_type(sample)
        if pattern_type and use_groups:
            _, grouped_pattern = self.common_patterns[pattern_type]
            if group_name:
                # Replace the default group name with custom one
                grouped_pattern = grouped_pattern.replace(f"<{pattern_type}>", f"<{group_name}>")
            return grouped_pattern
        elif pattern_type:
            match_pattern, grouped_pattern = self.common_patterns[pattern_type]
            # Return ungrouped version
            return grouped_pattern.replace(r"(?P<\w+>", "").replace(")", "")
        
        # Fallback: rule-based generation
        return self._build_fallback_regex(sample, group_name, use_groups)
    
    def _build_fallback_regex(self, sample: str, group_name: str = None, use_groups: bool = True) -> str:
        """Build regex using character-by-character analysis."""
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
    
    def build_complex_regex(self, samples: List[Tuple[str, str]]) -> str:
        """
        Build a complex regex from multiple samples with their group names.
        samples: List of (sample_text, group_name) tuples
        """
        if not samples:
            return ""
        
        patterns = []
        for sample_text, group_name in samples:
            if sample_text.strip():
                pattern = self.build_smart_regex(sample_text.strip(), group_name, use_groups=True)
                patterns.append(pattern)
        
        return "".join(patterns)
    
    def extract_groups_from_regex(self, regex_pattern: str) -> List[str]:
        """Extract all named group names from a regex pattern."""
        group_pattern = r'\(\?P<(\w+)>'
        return re.findall(group_pattern, regex_pattern)


class RegexProcessor(QThread):
    """Thread for processing files with regex patterns."""
    
    progress_updated = Signal(int)
    status_updated = Signal(str)
    results_ready = Signal(list)
    finished_processing = Signal()
    
    def __init__(self, regex_patterns: List[str], folder_path: str, file_extensions: List[str]):
        super().__init__()
        self.regex_patterns = regex_patterns
        self.folder_path = folder_path
        self.file_extensions = file_extensions
        self.results = []
    
    def run(self):
        """Process files with regex patterns."""
        try:
            files = self._get_files()
            total_files = len(files)
            
            if total_files == 0:
                self.status_updated.emit("No matching files found.")
                return
            
            self.status_updated.emit(f"Processing {total_files} files...")
            
            for i, file_path in enumerate(files):
                self._process_file(file_path)
                progress = int(((i + 1) / total_files) * 100)
                self.progress_updated.emit(progress)
                self.status_updated.emit(f"Processed: {file_path.name}")
            
            self.results_ready.emit(self.results)
            self.status_updated.emit(f"Completed! Found {len(self.results)} matches.")
            
        except Exception as e:
            self.status_updated.emit(f"Error: {str(e)}")
        finally:
            self.finished_processing.emit()
    
    def _get_files(self) -> List[Path]:
        """Get all files with specified extensions from the folder."""
        folder = Path(self.folder_path)
        files = []
        
        for ext in self.file_extensions:
            files.extend(folder.rglob(f"*.{ext}"))
        
        return files
    
    def _process_file(self, file_path: Path):
        """Process a single file with all regex patterns."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            line_number = 0
            for line in content.split('\n'):
                line_number += 1
                for pattern in self.regex_patterns:
                    try:
                        matches = re.finditer(pattern, line)
                        for match in matches:
                            result = {
                                'file': str(file_path),
                                'line_number': line_number,
                                'line_content': line.strip(),
                                'pattern': pattern,
                                'full_match': match.group(0),
                                'match_start': match.start(),
                                'match_end': match.end()
                            }
                            
                            # Add named groups if they exist
                            if match.groupdict():
                                result.update(match.groupdict())
                            
                            self.results.append(result)
                            
                    except re.error as e:
                        self.status_updated.emit(f"Invalid regex pattern: {pattern} - {str(e)}")
                        
        except Exception as e:
            self.status_updated.emit(f"Error processing {file_path}: {str(e)}")


class RegexGeneratorApp(QMainWindow):
    """Main application window for the regex generator."""
    
    def __init__(self):
        super().__init__()
        self.regex_builder = RegexBuilder(self)
        self.regex_patterns = []
        self.results = []
        self.processor_thread = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Dynamic Regex Generator with Grouping")
        self.setGeometry(100, 100, 1400, 900)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - Pattern building
        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Results
        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([700, 700])
        
    def _create_left_panel(self) -> QWidget:
        """Create the left panel for pattern building."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Pattern Builder Group
        builder_group = QGroupBox("Pattern Builder")
        builder_layout = QVBoxLayout(builder_group)
        
        # Sample input
        sample_layout = QHBoxLayout()
        sample_layout.addWidget(QLabel("Sample Text:"))
        self.sample_input = QLineEdit()
        self.sample_input.setPlaceholderText("Enter sample text to generate regex pattern...")
        sample_layout.addWidget(self.sample_input)
        builder_layout.addLayout(sample_layout)
        
        # Group name input
        group_layout = QHBoxLayout()
        group_layout.addWidget(QLabel("Group Name:"))
        self.group_name_input = QLineEdit()
        self.group_name_input.setPlaceholderText("Optional group name for capturing...")
        group_layout.addWidget(self.group_name_input)
        builder_layout.addLayout(group_layout)
        
        # Use groups checkbox
        self.use_groups_checkbox = QCheckBox("Generate with named groups")
        self.use_groups_checkbox.setChecked(True)
        builder_layout.addWidget(self.use_groups_checkbox)
        
        # Generated pattern display
        builder_layout.addWidget(QLabel("Generated Pattern:"))
        self.generated_pattern = QLineEdit()
        self.generated_pattern.setReadOnly(True)
        self.generated_pattern.setStyleSheet("background-color: #f0f0f0;")
        builder_layout.addWidget(self.generated_pattern)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.generate_btn = QPushButton("Generate Pattern")
        self.generate_btn.clicked.connect(self.generate_pattern)
        button_layout.addWidget(self.generate_btn)
        
        self.add_pattern_btn = QPushButton("Add to List")
        self.add_pattern_btn.clicked.connect(self.add_pattern_to_list)
        button_layout.addWidget(self.add_pattern_btn)
        builder_layout.addLayout(button_layout)
        
        layout.addWidget(builder_group)
        
        # Manual Pattern Input Group
        manual_group = QGroupBox("Manual Pattern Input")
        manual_layout = QVBoxLayout(manual_group)
        
        manual_layout.addWidget(QLabel("Regex Pattern:"))
        self.manual_pattern_input = QLineEdit()
        self.manual_pattern_input.setPlaceholderText("Enter regex pattern manually...")
        manual_layout.addWidget(self.manual_pattern_input)
        
        self.add_manual_btn = QPushButton("Add Manual Pattern")
        self.add_manual_btn.clicked.connect(self.add_manual_pattern)
        manual_layout.addWidget(self.add_manual_btn)
        
        layout.addWidget(manual_group)
        
        # Pattern List Group
        list_group = QGroupBox("Regex Patterns")
        list_layout = QVBoxLayout(list_group)
        
        self.pattern_list = QListWidget()
        list_layout.addWidget(self.pattern_list)
        
        list_buttons = QHBoxLayout()
        self.remove_pattern_btn = QPushButton("Remove Selected")
        self.remove_pattern_btn.clicked.connect(self.remove_selected_pattern)
        list_buttons.addWidget(self.remove_pattern_btn)
        
        self.clear_patterns_btn = QPushButton("Clear All")
        self.clear_patterns_btn.clicked.connect(self.clear_all_patterns)
        list_buttons.addWidget(self.clear_patterns_btn)
        list_layout.addLayout(list_buttons)
        
        layout.addWidget(list_group)
        
        # Processing Group
        process_group = QGroupBox("File Processing")
        process_layout = QVBoxLayout(process_group)
        
        # Folder selection
        folder_layout = QHBoxLayout()
        self.folder_path_label = QLabel("No folder selected")
        folder_layout.addWidget(self.folder_path_label)
        self.select_folder_btn = QPushButton("Select Folder")
        self.select_folder_btn.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.select_folder_btn)
        process_layout.addLayout(folder_layout)
        
        # File extensions
        ext_layout = QHBoxLayout()
        ext_layout.addWidget(QLabel("File Extensions:"))
        self.extensions_input = QLineEdit("txt,log,csv")
        self.extensions_input.setPlaceholderText("Comma-separated extensions...")
        ext_layout.addWidget(self.extensions_input)
        process_layout.addLayout(ext_layout)
        
        # Process button and progress
        self.process_btn = QPushButton("Process Files")
        self.process_btn.clicked.connect(self.process_files)
        process_layout.addWidget(self.process_btn)
        
        self.progress_bar = QProgressBar()
        process_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready")
        process_layout.addWidget(self.status_label)
        
        layout.addWidget(process_group)
        
        return panel
    
    def _create_right_panel(self) -> QWidget:
        """Create the right panel for results display."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Results Group
        results_group = QGroupBox("Results")
        results_layout = QVBoxLayout(results_group)
        
        # Results display
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)
        self.results_display.setFont(QFont("Consolas", 9))
        results_layout.addWidget(self.results_display)
        
        # Export buttons
        export_layout = QHBoxLayout()
        self.export_csv_btn = QPushButton("Export to CSV")
        self.export_csv_btn.clicked.connect(self.export_to_csv)
        self.export_csv_btn.setEnabled(False)
        export_layout.addWidget(self.export_csv_btn)
        
        self.clear_results_btn = QPushButton("Clear Results")
        self.clear_results_btn.clicked.connect(self.clear_results)
        export_layout.addWidget(self.clear_results_btn)
        results_layout.addLayout(export_layout)
        
        layout.addWidget(results_group)
        
        return panel
    
    def generate_pattern(self):
        """Generate regex pattern from sample text."""
        sample = self.sample_input.text().strip()
        group_name = self.group_name_input.text().strip()
        use_groups = self.use_groups_checkbox.isChecked()
        
        if not sample:
            QMessageBox.warning(self, "Warning", "Please enter sample text.")
            return
        
        pattern = self.regex_builder.build_smart_regex(sample, group_name, use_groups)
        self.generated_pattern.setText(pattern)
    
    def add_pattern_to_list(self):
        """Add generated pattern to the list."""
        pattern = self.generated_pattern.text().strip()
        if pattern and pattern not in self.regex_patterns:
            self.regex_patterns.append(pattern)
            self.pattern_list.addItem(pattern)
            self.generated_pattern.clear()
            self.sample_input.clear()
            self.group_name_input.clear()
    
    def add_manual_pattern(self):
        """Add manually entered pattern to the list."""
        pattern = self.manual_pattern_input.text().strip()
        if pattern and pattern not in self.regex_patterns:
            try:
                # Test if pattern is valid
                re.compile(pattern)
                self.regex_patterns.append(pattern)
                self.pattern_list.addItem(pattern)
                self.manual_pattern_input.clear()
            except re.error as e:
                QMessageBox.warning(self, "Invalid Regex", f"Invalid regex pattern: {str(e)}")
    
    def remove_selected_pattern(self):
        """Remove selected pattern from the list."""
        current_row = self.pattern_list.currentRow()
        if current_row >= 0:
            self.pattern_list.takeItem(current_row)
            del self.regex_patterns[current_row]
    
    def clear_all_patterns(self):
        """Clear all patterns from the list."""
        self.pattern_list.clear()
        self.regex_patterns.clear()
    
    def select_folder(self):
        """Select folder for file processing."""
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_path = folder
            self.folder_path_label.setText(f"Selected: {folder}")
    
    def process_files(self):
        """Process files with regex patterns."""
        if not self.regex_patterns:
            QMessageBox.warning(self, "Warning", "Please add at least one regex pattern.")
            return
        
        if not hasattr(self, 'folder_path') or not self.folder_path:
            QMessageBox.warning(self, "Warning", "Please select a folder.")
            return
        
        extensions = [ext.strip() for ext in self.extensions_input.text().split(',')]
        
        # Disable process button during processing
        self.process_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        
        # Start processing thread
        self.processor_thread = RegexProcessor(self.regex_patterns, self.folder_path, extensions)
        self.processor_thread.progress_updated.connect(self.progress_bar.setValue)
        self.processor_thread.status_updated.connect(self.status_label.setText)
        self.processor_thread.results_ready.connect(self.display_results)
        self.processor_thread.finished_processing.connect(self.processing_finished)
        self.processor_thread.start()
    
    def display_results(self, results: List[Dict[str, Any]]):
        """Display processing results."""
        self.results = results
        
        if not results:
            self.results_display.setText("No matches found.")
            return
        
        # Group results by file
        results_by_file = {}
        for result in results:
            file_path = result['file']
            if file_path not in results_by_file:
                results_by_file[file_path] = []
            results_by_file[file_path].append(result)
        
        # Format results for display
        display_text = f"Found {len(results)} matches in {len(results_by_file)} files:\n\n"
        
        for file_path, file_results in results_by_file.items():
            display_text += f"📁 {file_path}\n"
            display_text += f"   {len(file_results)} matches\n\n"
            
            for result in file_results[:5]:  # Show first 5 matches per file
                display_text += f"   Line {result['line_number']}: {result['full_match']}\n"
                
                # Show named groups if available
                groups = {k: v for k, v in result.items() 
                         if k not in ['file', 'line_number', 'line_content', 'pattern', 
                                    'full_match', 'match_start', 'match_end']}
                if groups:
                    display_text += f"   Groups: {groups}\n"
                
            if len(file_results) > 5:
                display_text += f"   ... and {len(file_results) - 5} more matches\n"
            
            display_text += "\n"
        
        self.results_display.setText(display_text)
        self.export_csv_btn.setEnabled(True)
    
    def processing_finished(self):
        """Re-enable process button after processing is complete."""
        self.process_btn.setEnabled(True)
        self.progress_bar.setValue(100)
    
    def export_to_csv(self):
        """Export results to CSV file."""
        if not self.results:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Results", "regex_results.csv", "CSV Files (*.csv)")
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                    if self.results:
                        fieldnames = list(self.results[0].keys())
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(self.results)
                
                QMessageBox.information(self, "Success", f"Results exported to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export results: {str(e)}")
    
    def clear_results(self):
        """Clear results display."""
        self.results_display.clear()
        self.results.clear()
        self.export_csv_btn.setEnabled(False)


if __name__ == "__main__":
    app = QApplication([])
    window = RegexGeneratorApp()
    window.show()
    app.exec()