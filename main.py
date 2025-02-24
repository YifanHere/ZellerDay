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
    if not delimiter:
        raise ValueError("日期格式错误或日期无效，无法识别分隔符。")
    parts = date_str.split(delimiter)
    # 当分隔符为 "-" 且字符串以负号开头时，split会产生一个空的首元素，需要处理
    if delimiter == "-" and date_str.startswith("-") and parts[0] == "":
        parts = ["-" + parts[1]] + parts[2:]
    if delimiter == "-" and not date_str.startswith("-") and len(parts) == 4 and parts[2] == "":
        parts = [parts[0], parts[1], "-" + parts[3]]
    if len(parts) != 3:
        raise ValueError("日期格式错误或日期无效，应包含三个部分。")
    # 如果第一部分以负号开头，直接认为它是年份
    if parts[0].startswith("-"):
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
    # 如果仍然无法确定年份则认为存在歧义
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

    # 提前处理公元前（负年份）的情况，避免重复提示
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

    # 处理正年份情况，使用 datetime 验证
    if year_index == 0:
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
                    print("输入 '1' 代表 日-月-年 (例如 2.3.2222 解析为 2222年3月2日)")
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
    new_date_str = delimiter.join(parts)
    try:
        date_obj = datetime.datetime.strptime(new_date_str, fmt)
        return date_obj.year, date_obj.month, date_obj.day
    except ValueError as e:
        raise ValueError("日期格式错误或日期无效，请检查日期数字。") from e

def calculate_weekday(year: int, month: int, day: int) -> int:
    """
    根据蔡勒公式计算星期几。针对不同历法分别使用：
    - 对于公历（1582年10月15日及之后）：公式为
        h = (day + floor((13*(month+1))/5) + year + floor(year/4) - floor(year/100) + floor(year/400)) % 7
    - 对于儒略历（1582年10月4日及之前）：公式为
        w = (y + floor(y/4) + floor(c/4) - 2c + floor(13*(month+1)/5) + day + 3) % 7
        其中 y = 年份后两位, c = 年份前两位
    对于处于转换空档期（1582年10月5日至10月14日）的日期，将抛出 ValueError。
    """
    if (year, month, day) >= (1582, 10, 15):
        # 使用公历公式
        if month < 3:
            month += 12
            year -= 1
        return (day + (13 * (month + 1)) // 5 + year + year // 4 - year // 100 + year // 400) % 7
    elif (year, month, day) <= (1582, 10, 4):
        # 使用儒略历公式
        if month < 3:
            month += 12
            year -= 1
        y = year % 100
        c = year // 100
        return (y + y // 4 + c // 4 - 2 * c + (13 * (month + 1)) // 5 + day + 3) % 7
    else:
        raise ValueError("输入日期处于历法转换空档期（1582年10月5日至10月14日）")

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

def is_valid_date(year: int, month: int, day: int) -> bool:
    """
    自定义验证日期合法性，不依赖 datetime.datetime，
    支持公元前（负年份）的情况。
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
        # 对于正年份使用 datetime 验证, 对于非正年份使用自定义验证
        if year > 0:
            try:
                datetime.datetime(year, month, day)
            except ValueError:
                error_msg = f"日期 '{date_str}' 不合法。"
                print(error_msg)
                new_lines.append(error_msg + "\n")
                continue
        else:
            if not is_valid_date(year, month, day):
                error_msg = f"日期 '{date_str}' 不合法。"
                print(error_msg)
                new_lines.append(error_msg + "\n")
                continue
        weekday_index = calculate_weekday(year, month, day)
        weekday_str = map_weekday(weekday_index)
        result_str = f"{date_str} -> {year:04d}年{month:02d}月{day:02d}日 是 {weekday_str}。"
        print(result_str)
        log_query(f"{year:04d}-{month:02d}-{day:02d}", weekday_str)
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
    else:
        try:
            year, month, day = validate_date_input(initial_input)
        except ValueError as ve:
            print(ve)
            return

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

    weekday_index = calculate_weekday(year, month, day)
    weekday_str = map_weekday(weekday_index)
    result_str = f"\n{year:04d}年{month:02d}月{day:02d}日 是 {weekday_str}。"
    print(result_str)
    log_query(f"{year:04d}-{month:02d}-{day:02d}", weekday_str)
    
    # 后续循环只显示“是否要继续计算其他日期？(Y/N/Enter):”
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
        else:
            try:
                year, month, day = validate_date_input(response)
            except ValueError as ve:
                print(ve)
                continue

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

        weekday_index = calculate_weekday(year, month, day)
        weekday_str = map_weekday(weekday_index)
        result_str = f"\n{year:04d}年{month:02d}月{day:02d}日 是 {weekday_str}。"
        print(result_str)
        log_query(f"{year:04d}-{month:02d}-{day:02d}", weekday_str)

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
        # 测试公元前日期
        self.assertEqual(validate_date_input("-1-1-1"), (-1, 1, 1))
        self.assertEqual(validate_date_input("-1.1.1"), (-1, 1, 1))

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        unittest.main(argv=[sys.argv[0]])
    else:
        main()