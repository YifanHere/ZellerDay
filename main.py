#!/usr/bin/env python3
"""
ZellerDay: 计算任一日期对应星期的程序
通过蔡勒公式计算日期对应的星期
"""

import datetime
import sys


def validate_date_input(date_str: str):
    """
    使用 datetime 模块验证日期字符串是否合法，格式要求为 YYYY-MM-DD。
    返回一个元组 (year, month, day)。
    如果格式错误或日期无效，则抛出 ValueError。
    """
    try:
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.year, date_obj.month, date_obj.day
    except ValueError as e:
        raise ValueError("日期格式错误或日期无效，请使用 YYYY-MM-DD 格式。") from e


def calculate_weekday(year: int, month: int, day: int) -> int:
    """
    根据蔡勒公式计算星期几。
    对于1月和2月，调整：将月份加 12，年份减 1。
    公式：
        h = (day + floor((13*(month+1))/5) + year + floor(year/4) - floor(year/100) + floor(year/400)) % 7
    返回 h 的值：
        0: 星期六, 1: 星期日, 2: 星期一, 3: 星期二,
        4: 星期三, 5: 星期四, 6: 星期五
    """
    if month < 3:
        month += 12
        year -= 1
    h = (day + (13 * (month + 1)) // 5 + year + year // 4 - year // 100 + year // 400) % 7
    return h


def map_weekday(h: int) -> str:
    """
    将 calculate_weekday 函数返回的结果映射为具体的星期名称。
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


def main():
    """
    程序入口函数。
    显示欢迎信息，循环获取用户输入，进行日期校验和结果输出。
    """
    print("欢迎使用 ZellerDay 星期计算器")
    print("该程序通过蔡勒公式计算任一日期对应的星期。")
    print("请输入日期，格式为 YYYY-MM-DD 或直接回车后按提示输入。")
    
    while True:
        user_input = input("\n请输入日期（如2025-02-24），或直接回车选择逐步输入：").strip()
        if user_input == "":
            try:
                year_input = input("请输入年份（例如2025）：").strip()
                month_input = input("请输入月份（例如2）：").strip()
                day_input = input("请输入日期（例如24）：").strip()
                year = int(year_input)
                month = int(month_input)
                day = int(day_input)
            except ValueError:
                print("输入无效，请输入数字。")
                continue
        else:
            try:
                year, month, day = validate_date_input(user_input)
            except ValueError as ve:
                print(ve)
                continue

        # 检查日期合法性：使用 datetime 模块再次校验
        try:
            datetime.datetime(year, month, day)
        except ValueError:
            print("输入的日期不合法。请检查月份、日期等是否正确。")
            continue

        weekday_index = calculate_weekday(year, month, day)
        weekday_str = map_weekday(weekday_index)
        print(f"\n{year}年{month}月{day}日 是 {weekday_str}。")

        again = input("\n是否要继续计算其他日期？(y/n): ").strip().lower()
        if again != "y":
            print("感谢使用，再见！")
            break


# 单元测试
import unittest

class TestZellerDay(unittest.TestCase):
    def test_calculate_weekday(self):
        # 测试2000-01-01，星期六
        self.assertEqual(calculate_weekday(2000, 1, 1), 0)
        # 测试2025-02-24，预期星期一 (返回值为2)
        self.assertEqual(calculate_weekday(2025, 2, 24), 2)
        # 测试2020-02-29，预期星期六 (返回值为0)
        self.assertEqual(calculate_weekday(2020, 2, 29), 0)
    
    def test_validate_date_input(self):
        # 正确格式
        self.assertEqual(validate_date_input("2025-02-24"), (2025, 2, 24))
        # 错误格式应抛出 ValueError
        with self.assertRaises(ValueError):
            validate_date_input("2025/02/24")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # 运行单元测试
        unittest.main(argv=[sys.argv[0]])
    else:
        main()