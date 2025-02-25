#!/usr/bin/env python3
"""
ZellerDay日期处理工具
包含日期验证、解析和格式化功能
"""

import datetime
import sys
from typing import Tuple, Optional

def validate_date_input(date_str: str) -> Tuple[int, int, int]:
    """
    使用 datetime 模块验证日期字符串是否合法。
    接受多种日期格式，包括但不限于：
      YYYY-MM-DD, YYYY.MM.DD, YYYY/MM/DD,
      DD-MM-YYYY, DD.MM.YYYY, DD/MM/YYYY,
      MM-DD-YYYY, MM.DD.YYYY, MM/DD/YYYY。
    对于存在歧义的输入（例如所有数字均小于等于31的情况，如 3-2-1），
    将通过交互提示让用户选择解析方式。
    返回一个元组 (year, month, day)。
    如果格式错误或日期无效，则抛出 ValueError。
    """
    date_str = date_str.strip()
    delimiter = None
    for d in ["-", "/", "."]:
        if date_str.count(d) == 2:
            delimiter = d
            break
    if delimiter is None:
        if date_str.startswith("-"):
            for d in ["-", "/", "."]:
                if d in date_str[1:]:
                    delimiter = d
                    break
        else:
            for d in ["-", "/", "."]:
                if d in date_str:
                    delimiter = d
                    break
    if not delimiter:
        raise ValueError("日期格式错误或日期无效，无法识别分隔符。")
    # 分割日期字符串
    parts = date_str.split(delimiter)
    # 当分隔符为 "-" 且字符串以负号开头时，split会产生一个空的首元素，需要处理
    if delimiter == "-" and date_str.startswith("-") and parts[0] == "":
        parts = ["-" + parts[1]] + parts[2:]
    if delimiter == "-" and not date_str.startswith("-") and len(parts) == 4 and parts[2] == "":
        parts = [parts[0], parts[1], "-" + parts[3]]
    if len(parts) != 3:
        raise ValueError("日期格式错误或日期无效，应包含三个部分。")
    # 如果三个部分完全相同，则无歧义，默认按 年-月-日 解析
    if parts[0] == parts[1] == parts[2]:
        year_index = 0
    # 如果第一部分以负号开头，直接认为它是年份
    elif parts[0].startswith("-"):
        year_index = 0
    else:
        year_index = None
        # 优先检测是否有4位年份或绝对值大于31（亦即不可能为日或月）的数字，包括负数情况
        for i, part in enumerate(parts):
            try:
                num = int(part)
            except ValueError:
                raise ValueError("日期格式错误或日期无效，包含非数字字符。")
            if len(part.lstrip("-")) == 4 or abs(num) > 31:
                year_index = i
                break
        if year_index is None and parts[2].startswith("-"):
            year_index = 2
        fmt_choice = None
        # 如果仍然无法确定年份，则提示用户选择解析方式
        if year_index is None:
            if sys.stdin.isatty():
                print("输入日期格式存在歧义，请选择解析方式:")
                print("输入 '1' 代表 年-月-日 (例如 3-2-1 解析为 3年2月1日)")
                print("输入 '2' 代表 日-月-年 (例如 3-2-1 解析为 1年2月3日)")
                print("输入 '3' 代表 月-日-年 (例如 3-2-1 解析为 1年3月2日)")
                choice = input("请输入对应序号 (默认1): ").strip()
                if choice == "2":
                    year_index = 2
                    fmt_choice = 2
                elif choice == "3":
                    year_index = 2
                    fmt_choice = 3
                else:
                    year_index = 0
            else:
                raise ValueError("日期格式错误或日期无效，无法确定年份。")
    # 针对负年份的处理：直接返回，不使用 datetime 验证
    try:
        int_year = int(parts[year_index])
    except ValueError:
        raise ValueError("日期格式错误或日期无效，包含非数字字符。")
    if int_year < 0:
        if year_index == 0:
            return int(parts[0]), int(parts[1]), int(parts[2])
        elif year_index == 2:
            try:
                a = int(parts[0])
                b = int(parts[1])
            except ValueError:
                raise ValueError("日期格式错误或日期无效，包含非数字字符。")
            if a <= 12 and b > 12:
                return int(parts[2]), int(parts[0]), int(parts[1])
            elif a <= 12 and b <= 12:
                if sys.stdin.isatty():
                    print("输入日期格式存在歧义，请选择解析方式:")
                    print("输入 '1' 代表 日-月-年")
                    print("输入 '2' 代表 月-日-年")
                    choice = input("请输入 1 或 2 (回车默认为 1): ").strip()
                    if choice == "2":
                        return int(parts[2]), int(parts[0]), int(parts[1])
                    else:
                        return int(parts[2]), int(parts[1]), int(parts[0])
                else:
                    return int(parts[2]), int(parts[1]), int(parts[0])
            elif a > 12 and b <= 12:
                return int(parts[2]), int(parts[1]), int(parts[0])
            else:
                raise ValueError("日期格式错误或日期无效，月份不可能大于12。")
        else:
            raise ValueError("日期格式错误或日期无效，无法识别年份位置。")
    # 处理正年份情况，使用 datetime 验证，并对各部分数字进行补零处理
    if year_index == 0:
        parts[0] = parts[0].zfill(4)
        parts[1] = parts[1].zfill(2)
        parts[2] = parts[2].zfill(2)
        fmt = f"%Y{delimiter}%m{delimiter}%d"
    elif year_index == 2:
        if fmt_choice is not None:
            if fmt_choice == 2:
                fmt = f"%d{delimiter}%m{delimiter}%Y"
            elif fmt_choice == 3:
                fmt = f"%m{delimiter}%d{delimiter}%Y"
            else:
                fmt = f"%Y{delimiter}%m{delimiter}%d"
        else:
            try:
                a = int(parts[0])
                b = int(parts[1])
            except ValueError:
                raise ValueError("日期格式错误或日期无效，包含非数字字符。")
            if a <= 12 and b > 12:
                fmt = f"%m{delimiter}%d{delimiter}%Y"
            elif a <= 12 and b <= 12:
                if sys.stdin.isatty():
                    print("输入日期格式存在歧义，请选择解析方式:")
                    print("输入 '1' 代表 日-月-日 (例如 2.3.2222 解析为 2222年3月2日)")  # Although it should be 日-月-年
                    print("输入 '2' 代表 月-日-年 (例如 2.3.2222 解析为 2222年2月3日)")
                    choice = input("请输入 1 或 2 (回车默认为 1): ").strip()
                    if choice == "2":
                        fmt = f"%m{delimiter}%d{delimiter}%Y"
                    else:
                        fmt = f"%d{delimiter}%m{delimiter}%Y"
                else:
                    fmt = f"%d{delimiter}%m{delimiter}%Y"
            elif a > 12 and b <= 12:
                fmt = f"%d{delimiter}%m{delimiter}%Y"
            else:
                raise ValueError("日期格式错误或日期无效，月份不可能大于12。")
        parts[2] = parts[2].zfill(4)
        parts[0] = parts[0].zfill(2)
        parts[1] = parts[1].zfill(2)
    new_date_str = delimiter.join(parts)
    try:
        date_obj = datetime.datetime.strptime(new_date_str, fmt)
        return date_obj.year, date_obj.month, date_obj.day
    except ValueError as e:
        raise ValueError("日期格式错误或日期无效，请检查日期数字。") from e

def is_valid_date(year: int, month: int, day: int) -> bool:
    """
    自定义验证日期合法性，不依赖 datetime.datetime，
    支持公元前（负年份）的情况。
    
    参数:
        year: 年份
        month: 月份
        day: 日期
        
    返回:
        布尔值表示日期是否合法
    """
    if not (1 <= month <= 12):
        return False
    if month in (1, 3, 5, 7, 8, 10, 12):
        max_day = 31
    elif month in (4, 6, 9, 11):
        max_day = 30
    elif month == 2:
        if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
            max_day = 29
        else:
            max_day = 28
    else:
        return False
    return 1 <= day <= max_day

def format_date(year: int, month: int, day: int) -> str:
    """
    格式化日期为标准显示格式
    
    参数:
        year: 年份
        month: 月份
        day: 日期
        
    返回:
        格式化的日期字符串
    """
    return f"{year:04d}年{month:02d}月{day:02d}日"