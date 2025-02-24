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
    使用 datetime 模块验证日期字符串是否合法。
    接受多种日期格式，包括但不限于：
      YYYY-MM-DD, YYYY.MM.DD, YYYY/MM/DD,
      DD-MM-YYYY, DD.MM.YYYY, DD/MM/YYYY,
      MM-DD-YYYY, MM.DD.YYYY, MM/DD/YYYY。
    对于存在歧义的输入（例如两个数字均小于等于12的情况，如 2.3.2222），将默认采用日-月-年格式。
    返回一个元组 (year, month, day)。
    如果格式错误或日期无效，则抛出 ValueError。
    """
    date_str = date_str.strip()
    delimiter = None
    for d in ["-", "/", "."]:
        if d in date_str:
            delimiter = d
            break
    if not delimiter:
        raise ValueError("日期格式错误或日期无效，无法识别分隔符。")
    parts = date_str.split(delimiter)
    if len(parts) != 3:
        raise ValueError("日期格式错误或日期无效，应包含三个部分。")
    year_index = None
    for i, part in enumerate(parts):
        try:
            num = int(part)
        except ValueError:
            raise ValueError("日期格式错误或日期无效，包含非数字字符。")
        if len(part) == 4 or num >= 1000:
            year_index = i
            break
    if year_index is None:
        raise ValueError("日期格式错误或日期无效，无法确定年份。")
    if year_index == 0:
        fmt = f"%Y{delimiter}%m{delimiter}%d"
    elif year_index == 2:
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
                print("输入 '1' 代表日-月-年 (例如 2.3.2222 解析为 2222年3月2日)")
                print("输入 '2' 代表月-日-年 (例如 2.3.2222 解析为 2222年2月3日)")
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
    else:
        raise ValueError("日期格式错误或日期无效，无法识别年份位置。")
    try:
        date_obj = datetime.datetime.strptime(date_str, fmt)
        return date_obj.year, date_obj.month, date_obj.day
    except ValueError as e:
        raise ValueError("日期格式错误或日期无效，请检查日期数字。") from e

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

def process_batch_file(file_path, mode_choice):
    """
    处理批量文件，根据模式选择导出结果到新文件或修改原文件。
    mode_choice: "1" 表示导出为新文件, "2" 表示修改原文件
    """
    if not os.path.exists(file_path):
        print(f"错误：文件 {file_path} 不存在。")
        return

    print(f"开始批量处理文件：{file_path}\n")
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        original_line = line.rstrip("\n")
        date_str = original_line.strip()
        if not date_str:
            new_lines.append("\n")
            continue
        try:
            year, month, day = validate_date_input(date_str)
        except ValueError as ve:
            error_msg = f"日期 '{date_str}' 无效：{ve}"
            print(error_msg)
            new_lines.append(error_msg + "\n")
            continue
        try:
            datetime.datetime(year, month, day)
        except ValueError:
            error_msg = f"日期 '{date_str}' 不合法。"
            print(error_msg)
            new_lines.append(error_msg + "\n")
            continue
        weekday_index = calculate_weekday(year, month, day)
        weekday_str = map_weekday(weekday_index)
        result_str = f"{date_str} -> {year}年{month}月{day}日 是 {weekday_str}。"
        print(result_str)
        log_query(date_str, weekday_str)
        new_lines.append(result_str + "\n")

    if mode_choice == "1":
        base, ext = os.path.splitext(file_path)
        new_file = f"{base}_result{ext}"
        with open(new_file, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"\n结果已导出至新文件：{new_file}")
    elif mode_choice == "2":
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        print(f"\n原文件 {file_path} 已被修改。")
    else:
        print("无效的处理模式。")

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
            print("请选择批量处理模式：")
            print("1. 将结果导出为新文件")
            print("2. 修改原文件")
            mode_choice = input("请输入 1 或 2：").strip()
            if mode_choice not in ("1", "2"):
                print("无效的选择。")
                return
            process_batch_file(file_path, mode_choice)
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
        # 测试多种正确格式
        self.assertEqual(validate_date_input("2025-02-24"), (2025, 2, 24))
        self.assertEqual(validate_date_input("2025/02/24"), (2025, 2, 24))
        self.assertEqual(validate_date_input("2025.2.24"), (2025, 2, 24))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=[sys.argv[0]])
    else:
        main()