#!/usr/bin/env python3
"""
ZellerDay命令行界面 | ZellerDay Command Line Interface
处理用户交互和命令行参数 | Handles user interaction and command line arguments
"""

import sys
import datetime
from typing import Tuple, Optional

from zeller_day.core import calculate_weekday, map_weekday
from zeller_day.date_utils import validate_date_input, is_valid_date, format_date
from zeller_day.io_utils import log_query, process_batch_file
from zeller_day.language import get_text, set_language, detect_language

def process_date(year: int, month: int, day: int) -> str:
    """
    处理日期并返回结果 | Process the date and return the result
    
    参数 | Parameters:
        year: 年份 | Year
        month: 月份 | Month
        day: 日期 | Day
        
    返回 | Returns:
        处理结果字符串 | Result string
    """
    weekday_index = calculate_weekday(year, month, day)
    weekday_str = map_weekday(weekday_index)
    formatted_date = format_date(year, month, day)
    result = get_text("result_format", formatted_date, weekday_str)
    log_query(f"{year:04d}-{month:02d}-{day:02d}", weekday_str)
    return result

def validate_and_process_date(date_input: str) -> Optional[str]:
    """
    验证日期输入并处理 | Validate date input and process
    
    参数 | Parameters:
        date_input: 日期输入字符串 | Date input string
        
    返回 | Returns:
        处理结果字符串，如果输入无效则返回None | Result string, or None if input is invalid
    """
    try:
        year, month, day = validate_date_input(date_input)
    except ValueError as ve:
        print(ve)
        return None
    
    # 验证日期合法性 | Validate date legality
    if year > 0:
        try:
            datetime.datetime(year, month, day)
        except ValueError:
            print(get_text("invalid_date"))
            return None
    else:
        if not is_valid_date(year, month, day):
            print(get_text("invalid_date"))
            return None
    
    return process_date(year, month, day)

def interactive_mode():
    """交互模式主循环 | Interactive mode main loop"""
    print(get_text("welcome"))
    print(get_text("intro"))
    
    # 初始输入提示，仅用于程序开始时 | Initial input prompt, only used at program start
    initial_input = input(get_text("input_date")).strip()
    if initial_input == "":
        try:
            year_input = input(get_text("input_year")).strip()
            month_input = input(get_text("input_month")).strip()
            day_input = input(get_text("input_day")).strip()
            year = int(year_input)
            month = int(month_input)
            day = int(day_input)
        except ValueError:
            print(get_text("invalid_input"))
            return
        
        # 验证日期合法性 | Validate date legality
        if year > 0:
            try:
                datetime.datetime(year, month, day)
            except ValueError:
                print(get_text("invalid_date"))
                return
        else:
            if not is_valid_date(year, month, day):
                print(get_text("invalid_date"))
                return
        
        result = process_date(year, month, day)
        print(f"\n{result}。")
    else:
        result = validate_and_process_date(initial_input)
        if result:
            print(f"\n{result}。")
        else:
            return
    
    # 后续循环只显示"是否要继续计算其他日期？(Y/N/Enter):" | Subsequent loops only display "Do you want to continue calculating other dates? (Y/N/Enter):"
    while True:
        response = input("\n" + get_text("continue")).strip()
        if response.lower() == "n":
            print(get_text("thanks"))
            break
        if response.lower() == "y" or response == "":
            try:
                year_input = input(get_text("input_year")).strip()
                month_input = input(get_text("input_month")).strip()
                day_input = input(get_text("input_day")).strip()
                year = int(year_input)
                month = int(month_input)
                day = int(day_input)
            except ValueError:
                print(get_text("invalid_input"))
                continue
            
            # 验证日期合法性 | Validate date legality
            if year > 0:
                try:
                    datetime.datetime(year, month, day)
                except ValueError:
                    print(get_text("invalid_date"))
                    continue
            else:
                if not is_valid_date(year, month, day):
                    print(get_text("invalid_date"))
                    continue
            
            result = process_date(year, month, day)
            print(f"\n{result}。")
        else:
            result = validate_and_process_date(response)
            if result:
                print(f"\n{result}。")

def main():
    """命令行入口函数 | Command line entry function"""
    # 检测并设置语言 | Detect and set language
    lang = detect_language()
    set_language(lang)
    
    if len(sys.argv) > 1:
        # 检查是否有语言参数 | Check if there are language parameters
        if sys.argv[1].lower() in ["--lang=zh", "--language=zh", "--zh"]:
            set_language("zh")
            sys.argv.pop(1)
        elif sys.argv[1].lower() in ["--lang=en", "--language=en", "--en"]:
            set_language("en")
            sys.argv.pop(1)
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "batch":
            if len(sys.argv) < 4:
                print(get_text("batch_mode"))
                print(get_text("batch_usage"))
                print(get_text("batch_modes"))
                return
            file_path = sys.argv[2]
            mode_choice = sys.argv[3]
            process_batch_file(file_path, mode_choice)
            return
        elif sys.argv[1] == "test":
            # 测试模式由主程序处理 | Test mode is handled by the main program
            return
    
    # 默认进入交互模式 | Default to interactive mode
    interactive_mode()

if __name__ == "__main__":
    main()