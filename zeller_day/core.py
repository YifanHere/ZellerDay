#!/usr/bin/env python3
"""
ZellerDay核心计算模块 | ZellerDay Core Calculation Module
包含蔡勒公式计算和星期映射功能 | Contains Zeller's formula calculation and weekday mapping functionality
"""

from zeller_day.language import get_text

def calculate_weekday(year: int, month: int, day: int) -> int:
    """
    使用蔡勒公式计算指定日期的星期 | Calculate the day of the week for a specified date using Zeller's formula
    
    参数 | Parameters:
        year: 年份（支持负数表示公元前） | Year (negative numbers represent BCE)
        month: 月份（1-12） | Month (1-12)
        day: 日期（1-31） | Day (1-31)
        
    返回 | Returns:
        整数表示的星期（0-6，对应星期六到星期五） | Integer representing the day of the week (0-6, corresponding to Saturday through Friday)
    """
    if year <= 0:
        calc_year = year + 1
        print(get_text("astronomical_year", year, calc_year))
    else:
        calc_year = year
    if (year, month, day) >= (1582, 10, 15):
        # 使用公历公式 | Using Gregorian calendar formula
        if month < 3:
            month += 12
            calc_year -= 1
        return (day + (13 * (month + 1)) // 5 + calc_year + calc_year // 4 - calc_year // 100 + calc_year // 400) % 7
    elif (year, month, day) <= (1582, 10, 4):
        # 使用儒略历公式 | Using Julian calendar formula
        if month < 3:
            month += 12
            calc_year -= 1
        y = calc_year % 100
        c = calc_year // 100
        return (y + y // 4 + c // 4 - 2 * c + (13 * (month + 1)) // 5 + day + 3) % 7
    else:
        raise ValueError(get_text("calendar_gap"))

def map_weekday(h: int) -> str:
    """
    将 calculate_weekday 函数返回的结果映射为具体的星期名称。 | Map the result returned by the calculate_weekday function to a specific weekday name.
    
    参数 | Parameters:
        h: 星期数字（0-6） | Weekday number (0-6)
        
    返回 | Returns:
        当前语言的星期名称 | Weekday name in the current language
    """
    weekdays = get_text("weekdays")
    if 0 <= h < len(weekdays):
        return weekdays[h]
    return get_text("unknown_weekday")