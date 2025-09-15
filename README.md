# MatchaRegex - Log File Search & Analysis

MatchaRegex is a desktop application for searching, analyzing, and exporting results from log files using advanced regular expressions. It features a modern UI built with PySide6 and supports dynamic regex pattern generation, named groups, and exporting results to Excel.

## Features

- **Folder Selection**: Choose a directory containing log files to search.
- **File Pattern Filtering**: Specify file patterns (wildcards, comma-separated) to limit which files are searched.
- **Regex Pattern Builder**: Convert sample text to regex patterns, including support for named groups.
- **Pattern List Management**: Add, remove, and clear regex patterns from the active search list.
- **Multiline Search**: Enable multiline regex search for line-by-line or whole-file matching.
- **Search Results Table**: View matches in a table with named group extraction.
- **Export to Excel**: Save search results to an Excel file with formatted tables.
- **System Output Panel**: View status messages and logs during processing.
- **Help & Resources**: Quick access to Regex101 and Regex Cheatsheet.

## Getting Started

### Prerequisites

- Python 3.12+
- [PySide6](https://pypi.org/project/PySide6/)
- [pandas](https://pypi.org/project/pandas/)
- [xlsxwriter](https://pypi.org/project/XlsxWriter/)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/MatchaRegex.git
    cd MatchaRegex
    ```

2. Install dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Run the application:
    ```sh
    python src/main.py
    ```

## Usage

1. **Select Folder**: Use the "Browse" button to choose a folder with log files.
2. **Set File Patterns**: Optionally enter file patterns (e.g., `*.log,*.txt`) to filter files.
3. **Build Regex**: Enter sample text and click "Convert" to generate a regex pattern.
4. **Manage Patterns**: Add generated or manual regex patterns to the search list.
5. **Start Search**: Click "Start Search" to process files and view results.
6. **Export Results**: Use "Export to Excel" to save results for further analysis.

## UI Overview

- **Input Panel**: Folder path, file pattern, sample-to-regex conversion, regex input.
- **Pattern List**: Active regex patterns for searching.
- **Results Panel**: Table of matches, export and clear buttons, row limit, multiline search toggle.
- **System Output**: Status messages and logs.

## Advanced Features

- **Named Groups**: Regex patterns with named groups are supported and extracted in results.
- **Multithreading**: File processing and export operations run in background threads for responsiveness.
- **Cross-Platform**: Works on Windows, macOS, and Linux.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements.

## License

MIT License

## Acknowledgements

- [PySide6](https://www.qt.io/qt-for-python)
- [pandas](https://pandas.pydata.org/)
- [XlsxWriter](https://xlsxwriter.readthedocs.io/)
- [Regex101](https://regex101.com/)
- [RegexLearn Cheatsheet](https://regexlearn.com/cheatsheet)

---
For more details, see the source code in [src/main.py](src/main.py), [src/modules/regex_builder.py](src/modules/regex_builder.py), and [src/modules/regex_processor.py](src/modules/regex_processor.py).