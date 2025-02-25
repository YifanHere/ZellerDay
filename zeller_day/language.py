#!/usr/bin/env python3
"""
ZellerDay语言配置模块 | ZellerDay Language Configuration Module
包含多语言支持和语言检测功能 | Contains multilingual support and language detection functionality
"""

import locale
import os
import sys
from typing import Dict, Any

# 语言配置 | Language configuration
TEXTS = {
    "zh": {  # 中文
        "welcome": "欢迎使用 ZellerDay 星期计算器",
        "intro": "该程序通过蔡勒公式计算任一日期对应星期。\n",
        "input_date": "请输入日期（如2025-02-24），或直接回车选择逐步输入：",
        "input_year": "请输入年份（例如2025 或 3 或 -123）：",
        "input_month": "请输入月份（例如2）：",
        "input_day": "请输入日期（例如24）：",
        "invalid_input": "输入无效，请输入数字。",
        "invalid_date": "输入的日期不合法。请检查月份、日期等是否正确。",
        "continue": "是否要继续计算其他日期？(Y/N/Enter): ",
        "thanks": "感谢使用，再见！",
        "result_format": "{} 是 {}",
        "batch_mode": "使用批量处理模式，需要指定文件名和处理模式。",
        "batch_usage": "用法: python main.py batch <文件路径> <处理模式>",
        "batch_modes": "处理模式: 1 - 导出到新文件, 2 - 修改原文件",
        "batch_start": "开始批量处理文件：{}",
        "file_not_exist": "错误：文件 {} 不存在。",
        "invalid_date_error": "日期 '{}' 无效：{}",
        "date_illegal": "日期 '{}' 不合法。",
        "batch_result": "{} -> {}年{:02d}月{:02d}日 是 {}。",
        "result_exported": "结果已导出至新文件：{}",
        "file_modified": "原文件 {} 已被修改。",
        "invalid_mode": "无效的处理模式。",
        "date_format_ambiguous": "输入日期格式存在歧义，请选择解析方式:",
        "format_ymd": "输入 '1' 代表 年-月-日 (例如 3-2-1 解析为 3年2月1日)",
        "format_dmy": "输入 '2' 代表 日-月-年 (例如 3-2-1 解析为 1年2月3日)",
        "format_mdy": "输入 '3' 代表 月-日-年 (例如 3-2-1 解析为 1年3月2日)",
        "choose_format": "请输入对应序号 (默认1): ",
        "format_dm_ambiguous": "输入日期格式存在歧义，请选择解析方式:",
        "format_dm_1": "输入 '1' 代表 日-月-年 (例如 2.3.2222 解析为 2222年3月2日)",
        "format_dm_2": "输入 '2' 代表 月-日-年 (例如 2.3.2222 解析为 2222年2月3日)",
        "choose_dm_format": "请输入 1 或 2 (回车默认为 1): ",
        "date_format_error": "日期格式错误或日期无效，",
        "no_delimiter": "无法识别分隔符。",
        "not_three_parts": "应包含三个部分。",
        "non_numeric": "包含非数字字符。",
        "cannot_determine_year": "无法确定年份。",
        "check_date_numbers": "请检查日期数字。",
        "cannot_identify_year": "无法识别年份位置。",
        "month_not_gt_12": "月份不可能大于12。",
        "calendar_gap": "输入日期处于历法转换空档期（1582年10月5日至10月14日）",
        "weekdays": ["星期六", "星期日", "星期一", "星期二", "星期三", "星期四", "星期五"],
        "unknown_weekday": "未知星期",
        "date_format": "{:04d}年{:02d}月{:02d}日",
        "astronomical_year": "[DEBUG] 天文转换: 原始年份 {} 转换为年 {}"
    },
    "en": {  # 英文
        "welcome": "Welcome to ZellerDay Weekday Calculator",
        "intro": "This program calculates the weekday for any date using Zeller's formula.\n",
        "input_date": "Please enter a date (e.g. 2025-02-24), or press Enter for step-by-step input: ",
        "input_year": "Please enter the year (e.g. 2025 or 3 or -123): ",
        "input_month": "Please enter the month (e.g. 2): ",
        "input_day": "Please enter the day (e.g. 24): ",
        "invalid_input": "Invalid input, please enter numbers.",
        "invalid_date": "The date entered is invalid. Please check if the month, day, etc. are correct.",
        "continue": "Do you want to calculate another date? (Y/N/Enter): ",
        "thanks": "Thank you for using ZellerDay, goodbye!",
        "result_format": "{} is {}",
        "batch_mode": "Using batch processing mode, you need to specify the filename and processing mode.",
        "batch_usage": "Usage: python main.py batch <file_path> <processing_mode>",
        "batch_modes": "Processing modes: 1 - Export to a new file, 2 - Modify the original file",
        "batch_start": "Starting batch processing of file: {}",
        "file_not_exist": "Error: File {} does not exist.",
        "invalid_date_error": "Date '{}' is invalid: {}",
        "date_illegal": "Date '{}' is illegal.",
        "batch_result": "{} -> {} is {}.",
        "result_exported": "Results have been exported to a new file: {}",
        "file_modified": "The original file {} has been modified.",
        "invalid_mode": "Invalid processing mode.",
        "date_format_ambiguous": "The date format is ambiguous, please choose an interpretation:",
        "format_ymd": "Enter '1' for Year-Month-Day (e.g. 3-2-1 interpreted as Year 3, Month 2, Day 1)",
        "format_dmy": "Enter '2' for Day-Month-Year (e.g. 3-2-1 interpreted as Year 1, Month 2, Day 3)",
        "format_mdy": "Enter '3' for Month-Day-Year (e.g. 3-2-1 interpreted as Year 1, Month 3, Day 2)",
        "choose_format": "Please enter the corresponding number (default 1): ",
        "format_dm_ambiguous": "The date format is ambiguous, please choose an interpretation:",
        "format_dm_1": "Enter '1' for Day-Month-Year (e.g. 2.3.2222 interpreted as Year 2222, Month 3, Day 2)",
        "format_dm_2": "Enter '2' for Month-Day-Year (e.g. 2.3.2222 interpreted as Year 2222, Month 2, Day 3)",
        "choose_dm_format": "Please enter 1 or 2 (Enter defaults to 1): ",
        "date_format_error": "Date format error or invalid date, ",
        "no_delimiter": "cannot recognize delimiter.",
        "not_three_parts": "should contain three parts.",
        "non_numeric": "contains non-numeric characters.",
        "cannot_determine_year": "cannot determine the year.",
        "check_date_numbers": "please check the date numbers.",
        "cannot_identify_year": "cannot identify the year position.",
        "month_not_gt_12": "month cannot be greater than 12.",
        "calendar_gap": "Input date is in the calendar conversion gap period (October 5-14, 1582)",
        "weekdays": ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
        "unknown_weekday": "Unknown weekday",
        "date_format": "{:04d}-{:02d}-{:02d}",
        "astronomical_year": "[DEBUG] Astronomical conversion: Original year {} converted to year {}"
    }
}

# 当前语言 | Current language
current_language = "en"  # 默认为英文 | Default to English

def detect_language() -> str:
    """
    检测用户的语言偏好 | Detect user's language preference
    
    返回 | Returns:
        语言代码 ("zh" 或 "en") | Language code ("zh" or "en")
    """
    # 尝试从环境变量获取语言设置 | Try to get language settings from environment variables
    env_lang = os.environ.get('LANG', '').lower()
    if 'zh' in env_lang or 'cn' in env_lang:
        return "zh"
    
    # 尝试从系统区域设置获取语言 | Try to get language from system locale settings
    try:
        system_locale = locale.getdefaultlocale()[0].lower()
        if 'zh' in system_locale or 'cn' in system_locale:
            return "zh"
    except (AttributeError, IndexError, TypeError):
        pass
    
    # 尝试从命令行参数获取语言设置 | Try to get language settings from command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ["--lang=zh", "--language=zh", "--zh"]:
            return "zh"
        elif sys.argv[1].lower() in ["--lang=en", "--language=en", "--en"]:
            return "en"
    
    # 如果无法确定，则进行简单的交互式检测 | If unable to determine, perform a simple interactive detection
    if sys.stdin.isatty():
        print("Please select your language / 请选择您的语言:")
        print("1. English")
        print("2. 中文")
        choice = input("Enter 1 or 2 / 输入 1 或 2 (default/默认: 2): ").strip()
        if choice == "1":
            return "en"
    
    # 默认返回英文 | Default to English
    return "en"

def set_language(lang_code: str) -> None:
    """
    设置当前语言 | Set the current language
    
    参数 | Parameters:
        lang_code: 语言代码 ("zh" 或 "en") | Language code ("zh" or "en")
    """
    global current_language
    if lang_code in TEXTS:
        current_language = lang_code
    else:
        current_language = "en"  # 默认为英文 | Default to English

def get_text(key: str, *args, **kwargs) -> str:
    """
    获取指定键的文本，并进行格式化 | Get the text for the specified key and format it
    
    参数 | Parameters:
        key: 文本键 | Text key
        *args, **kwargs: 格式化参数 | Formatting parameters
        
    返回 | Returns:
        格式化后的文本 | Formatted text
    """
    text = TEXTS.get(current_language, TEXTS["zh"]).get(key, key)
    if args or kwargs:
        try:
            return text.format(*args, **kwargs)
        except (IndexError, KeyError):
            return text
    return text

# 初始化语言设置 | Initialize language settings
set_language(detect_language())