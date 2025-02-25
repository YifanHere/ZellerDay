#!/usr/bin/env python3
"""
ZellerDay核心计算模块
包含蔡勒公式计算和星期映射功能
"""

def calculate_weekday(year: int, month: int, day: int) -> int:
    """
    使用蔡勒公式计算指定日期的星期
    
    参数:
        year: 年份（支持负数表示公元前）
        month: 月份（1-12）
        day: 日期（1-31）
        
    返回:
        整数表示的星期（0-6，对应星期六到星期五）
    """
    if year <= 0:
        calc_year = year + 1
        print(f"[DEBUG] 天文转换: 原始年份 {year} 转换为年 {calc_year}")
    else:
        calc_year = year
    if (year, month, day) >= (1582, 10, 15):
        # 使用公历公式
        if month < 3:
            month += 12
            calc_year -= 1
        return (day + (13 * (month + 1)) // 5 + calc_year + calc_year // 4 - calc_year // 100 + calc_year // 400) % 7
    elif (year, month, day) <= (1582, 10, 4):
        # 使用儒略历公式
        if month < 3:
            month += 12
            calc_year -= 1
        y = calc_year % 100
        c = calc_year // 100
        return (y + y // 4 + c // 4 - 2 * c + (13 * (month + 1)) // 5 + day + 3) % 7
    else:
        raise ValueError("输入日期处于历法转换空档期（1582年10月5日至10月14日）")

def map_weekday(h: int) -> str:
    """
    将 calculate_weekday 函数返回的结果映射为具体的星期名称。
    
    参数:
        h: 星期数字（0-6）
        
    返回:
        中文星期名称
    """
    mapping = {
        0: "星期六",
        1: "星期日",
        2: "星期一",
        3: "星期二",
        4: "星期三",
        5: "星期四",
        6: "星期五"
    }
    return mapping.get(h, "未知星期")