#!/usr/bin/env python3
"""
ZellerDay命令行界面
处理用户交互和命令行参数
"""

import sys
import datetime
from typing import Tuple, Optional

from zeller_day.core import calculate_weekday, map_weekday
from zeller_day.date_utils import validate_date_input, is_valid_date, format_date
from zeller_day.io_utils import log_query, process_batch_file

def process_date(year: int, month: int, day: int) -> str:
    """
    处理日期并返回结果
    
    参数:
        year: 年份
        month: 月份
        day: 日期
        
    返回:
        处理结果字符串
    """
    weekday_index = calculate_weekday(year, month, day)
    weekday_str = map_weekday(weekday_index)
    formatted_date = format_date(year, month, day)
    result = f"{formatted_date} 是 {weekday_str}"
    log_query(f"{year:04d}-{month:02d}-{day:02d}", weekday_str)
    return result

def validate_and_process_date(date_input: str) -> Optional[str]:
    """
    验证日期输入并处理
    
    参数:
        date_input: 日期输入字符串
        
    返回:
        处理结果字符串，如果输入无效则返回None
    """
    try:
        year, month, day = validate_date_input(date_input)
    except ValueError as ve:
        print(ve)
        return None
    
    # 验证日期合法性
    if year > 0:
        try:
            datetime.datetime(year, month, day)
        except ValueError:
            print("输入的日期不合法。请检查月份、日期等是否正确。")
            return None
    else:
        if not is_valid_date(year, month, day):
            print("输入的日期不合法。请检查月份、日期等是否正确。")
            return None
    
    return process_date(year, month, day)

def interactive_mode():
    """交互模式主循环"""
    print("欢迎使用 ZellerDay 星期计算器")
    print("该程序通过蔡勒公式计算任一日期对应星期。\n")
    
    # 初始输入提示，仅用于程序开始时
    initial_input = input("请输入日期（如2025-02-24），或直接回车选择逐步输入：").strip()
    if initial_input == "":
        try:
            year_input = input("请输入年份（例如2025 或 3 或 -123）：").strip()
            month_input = input("请输入月份（例如2）：").strip()
            day_input = input("请输入日期（例如24）：").strip()
            year = int(year_input)
            month = int(month_input)
            day = int(day_input)
        except ValueError:
            print("输入无效，请输入数字。")
            return
        
        # 验证日期合法性
        if year > 0:
            try:
                datetime.datetime(year, month, day)
            except ValueError:
                print("输入的日期不合法。请检查月份、日期等是否正确。")
                return
        else:
            if not is_valid_date(year, month, day):
                print("输入的日期不合法。请检查月份、日期等是否正确。")
                return
        
        result = process_date(year, month, day)
        print(f"\n{result}。")
    else:
        result = validate_and_process_date(initial_input)
        if result:
            print(f"\n{result}。")
        else:
            return
    
    # 后续循环只显示"是否要继续计算其他日期？(Y/N/Enter):"
    while True:
        response = input("\n是否要继续计算其他日期？(Y/N/Enter): ").strip()
        if response.lower() == "n":
            print("感谢使用，再见！")
            break
        if response.lower() == "y" or response == "":
            try:
                year_input = input("请输入年份（例如2025 或 3 或 -123）：").strip()
                month_input = input("请输入月份（例如2）：").strip()
                day_input = input("请输入日期（例如24）：").strip()
                year = int(year_input)
                month = int(month_input)
                day = int(day_input)
            except ValueError:
                print("输入无效，请输入数字。")
                continue
            
            # 验证日期合法性
            if year > 0:
                try:
                    datetime.datetime(year, month, day)
                except ValueError:
                    print("输入的日期不合法。请检查月份、日期等是否正确。")
                    continue
            else:
                if not is_valid_date(year, month, day):
                    print("输入的日期不合法。请检查月份、日期等是否正确。")
                    continue
            
            result = process_date(year, month, day)
            print(f"\n{result}。")
        else:
            result = validate_and_process_date(response)
            if result:
                print(f"\n{result}。")

def main():
    """命令行入口函数"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "batch":
            if len(sys.argv) < 4:
                print("使用批量处理模式，需要指定文件名和处理模式。")
                print("用法: python main.py batch <文件路径> <处理模式>")
                print("处理模式: 1 - 导出到新文件, 2 - 修改原文件")
                return
            file_path = sys.argv[2]
            mode_choice = sys.argv[3]
            process_batch_file(file_path, mode_choice)
            return
        elif sys.argv[1] == "test":
            # 测试模式由主程序处理
            return
    
    # 默认进入交互模式
    interactive_mode()

if __name__ == "__main__":
    main()