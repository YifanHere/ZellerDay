# ZellerDay 📅→📆

**Quickly Calculate the Day of Week for Any Date Using Zeller's Congruence | Elegant and Concise Command Line Tool**

**[中文文档](README_zh.md)**
---

## ✨ Project Overview

ZellerDay is a Python-based tool that uses the classic [Zeller's Congruence](https://en.wikipedia.org/wiki/Zeller%27s_congruence) to calculate the day of the week for any given date.
With its built-in date parsing functionality, the program supports various common date formats and provides interactive prompts when encountering ambiguous inputs to help users select the appropriate parsing method.
The project is feature-complete, with clean and standardized code, making it suitable as a teaching or self-learning example.

---

## 🚀 Features
- ✔️ **High Calculation Compatibility**: Supports calculating the day of the week for **any date** (except non-existent dates) using Zeller's formula, **compatible with both BCE and CE dates (negative years)**
- 🔢 **High Input Compatibility**: When input is ambiguous (e.g., all values are less than or equal to 31), the program interactively prompts users to select the correct parsing method
- 📊 **Calendar Conversion Handling**: Automatically handles the conversion between Gregorian and Julian calendars, using the Julian calendar formula for dates on or before October 4, 1582, and the Gregorian calendar formula for dates on or after October 15, 1582
- 📌 **Two Input Modes**: Supports both one-time complete date input or step-by-step year, month, and day input
- ⚡ **Batch Date File Processing**: Built-in batch processing functionality can read dates from each line of a text file, perform calculations, and export to a new file or modify the original file based on user choice
- 🔁 **Logging**: All date query results are recorded in the data/logs/query_history.log file, with the format "timestamp - query -> result"
- 🌐 **Multilingual Support**: Automatically detects the user's language environment and provides the appropriate interface language (Chinese or English), or allows manual language selection via command line parameters
- 📚 **Zero Third-party Dependencies**: 100% pure Python implementation
- 🛡️ **Multiple Date Input Formats**: The program supports various date formats, including but not limited to:
  - YYYY-MM-DD
  - YYYY/MM/DD
  - YYYY.MM.DD
  - DD-MM-YYYY
  - DD/MM/YYYY
  - DD.MM.YYYY
  - And other formats

---

## 📂 Project Structure

```
ZellerDay/
├── data/                  # Data directory
│   └── logs/              # Log storage directory
├── tests/                 # Test directory
│   ├── __init__.py
│   └── test_zeller_day.py # Unit test file
├── zeller_day/            # Main source code directory
│   ├── __init__.py
│   ├── cli.py             # Command line interface module
│   ├── core.py            # Core calculation module (Zeller's formula implementation)
│   ├── date_utils.py      # Date processing utilities
│   ├── io_utils.py        # Input/output utilities
│   └── language.py        # Language configuration module (multilingual support)
├── .gitignore
├── LICENSE.md
├── main.py                # Program entry point
├── README.md
└── requirements.txt
```

---

## 💡 Usage Tips

- When the month or day is a single digit, the input will be automatically zero-padded. For example, 233-1-1 will be automatically converted to 0233-01-01

- BC Date Processing:
  - The program supports calculating BC dates, just enter a negative year, e.g. -1414/5/14 for May 14, 1414 BC
  - The BC date displays astronomical conversion information on the console, e.g. "[DEBUG] Astronomical conversion: Original year -1414 to year -1413"

- The batch date file processing feature supports not only txt format but any text file where dates can be read line by line. For example, .txt, .csv, .log, and other text formats are all supported

- Batch Processing Mode:  
  - The program supports batch processing of date files using the following command:
    ```bash
    python main.py batch <file_path> <processing_mode>
    ```
  - Processing modes:
    - 1 - Export to a new file (generates original_filename_result.extension)
    - 2 - Modify the original file

- Dates in batch files should be arranged with one date per line, in supported formats such as YYYY-MM-DD, YYYY/MM/DD, or YYYY.MM.DD, separated by line breaks
  - For example, a compliant batch date file might contain:
    >```bash
    >2025-01-01
    >2025-02-14
    >2025-03-15
    >2025-04-01
    >2025-05-01
    >```

---

## 📦 Quick Start

### Requirements
- Python 3.x

### Installation
```bash
# Clone the repository
git clone https://github.com/YifanHere/ZellerDay.git
cd ZellerDay

# No additional dependencies required
```

### Running the Program
```bash
# Interactive mode
python main.py

# Specify language (Chinese)
python main.py --lang=zh

# Specify language (English)
python main.py --lang=en

# Batch processing mode
python main.py batch <file_path> <processing_mode>
# Example: python main.py batch dates.txt 1

# Batch processing mode with language specification
python main.py --lang=en batch <file_path> <processing_mode>
```

### Usage Example

**English Interface (default or using --lang=en parameter)**
```
Welcome to ZellerDay Weekday Calculator
This program calculates the weekday for any date using Zeller's formula.

Please enter a date (e.g. 2025-02-24), or press Enter for step-by-step input: 2025-2-24

2025-02-24 is Monday.

Do you want to calculate another date? (Y/N/Enter):
Please enter the year (e.g. 2025 or 3 or -123): 5201
Please enter the month (e.g. 2): 3
Please enter the day (e.g. 24): 14

5201-03-14 is Wednesday.

Do you want to calculate another date? (Y/N/Enter): -1414/5/14
[DEBUG] Astronomical conversion: Original year -1414 converted to year -1413

-1414-05-14 is Thursday.

Do you want to calculate another date? (Y/N/Enter): n
Thank you for using ZellerDay, goodbye!
```

**Chinese Interface (using --lang=zh parameter)**
```
欢迎使用 ZellerDay 星期计算器
该程序通过蔡勒公式计算任一日期对应星期。

请输入日期（如2025-02-24），或直接回车选择逐步输入：2025-2-24

2025年02月24日 是 星期一。

是否要继续计算其他日期？(Y/N/Enter):
请输入年份（例如2025 或 3 或 -123）：5201
请输入月份（例如2）：3
请输入日期（例如24）：14

5201年03月14日 是 星期三。

是否要继续计算其他日期？(Y/N/Enter): n
感谢使用，再见！
```

---

## 🧪 Running Tests

The project includes comprehensive unit tests that can be run using the following command:

```bash
# Run from the project root directory
python -m unittest discover tests
```

The tests cover key components including core calculation functionality, date validation and parsing, and weekday mapping.

---

## 🔧 Developer's Guide

### Code Structure

- **core.py**: Contains the implementation of Zeller's formula and weekday mapping functionality
- **date_utils.py**: Contains date validation, parsing, and formatting functionality
- **io_utils.py**: Contains logging and batch file processing functionality
- **cli.py**: Contains command line interface and user interaction functionality
- **language.py**: Contains multilingual support, language detection, and text localization functionality

### Contribution Guidelines

1. Fork this repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details