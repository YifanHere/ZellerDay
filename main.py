#!/usr/bin/env python3
"""
ZellerDay: 计算任一日期对应星期的程序
通过蔡勒公式计算日期对应的星期
"""

import datetime
import sys
import os

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

def log_query(query: str, result: str):
    """
    将日期查询记录写入到 query_history.log 文件。
    格式：timestamp - query -> result
    """
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{now} - {query} -> {result}\n"
    with open("query_history.log", "a", encoding="utf-8") as f:
        f.write(log_line)

def main():
    """
    程序入口函数。
    根据命令行参数支持查询历史与批量文件处理功能，若无参数则进入交互模式。
    """
    print("欢迎使用 ZellerDay 星期计算器")
    print("该程序通过蔡勒公式计算任一日期对应星期。\n")
    if len(sys.argv) > 1:
        if sys.argv[1] == "history":
            if os.path.exists("query_history.log"):
                print("查询历史记录：\n")
                with open("query_history.log", "r", encoding="utf-8") as f:
                    print(f.read())
            else:
                print("无查询历史记录。")
            return
        elif sys.argv[1] == "batch":
            if len(sys.argv) < 3:
                print("错误：请指定包含日期的批量文件路径。")
                return
            file_path = sys.argv[2]
            if not os.path.exists(file_path):
                print(f"错误：文件 {file_path} 不存在。")
                return
            print(f"开始批量处理文件：{file_path}\n")
            with open(file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines:
                date_str = line.strip()
                if not date_str:
                    continue
                try:
                    year, month, day = validate_date_input(date_str)
                except ValueError as ve:
                    print(f"日期 '{date_str}' 无效：{ve}")
                    continue
                try:
                    datetime.datetime(year, month, day)
                except ValueError:
                    print(f"日期 '{date_str}' 不合法。")
                    continue
                weekday_index = calculate_weekday(year, month, day)
                weekday_str = map_weekday(weekday_index)
                result_str = f"{year}年{month}月{day}日 是 {weekday_str}。"
                print(result_str)
                log_query(date_str, weekday_str)
            return

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

        try:
            datetime.datetime(year, month, day)
        except ValueError:
            print("输入的日期不合法。请检查月份、日期等是否正确。")
            continue

        weekday_index = calculate_weekday(year, month, day)
        weekday_str = map_weekday(weekday_index)
        result_str = f"\n{year}年{month}月{day}日 是 {weekday_str}。"
        print(result_str)
        log_query(f"{year}-{month:02d}-{day:02d}", weekday_str)

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