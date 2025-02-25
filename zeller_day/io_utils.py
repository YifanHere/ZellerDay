#!/usr/bin/env python3
"""
ZellerDay输入输出工具
包含日志记录和文件处理功能
"""

import os
import datetime
from typing import List, Tuple
from pathlib import Path

from zeller_day.date_utils import validate_date_input, is_valid_date
from zeller_day.core import calculate_weekday, map_weekday

# 日志目录
LOG_DIR = Path("data") / "logs"

def ensure_log_dir():
    """确保日志目录存在"""
    os.makedirs(LOG_DIR, exist_ok=True)

def log_query(query: str, result: str):
    """
    记录日期查询到日志文件
    
    参数:
        query: 查询内容
        result: 查询结果
    """
    ensure_log_dir()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"{now} - {query} -> {result}\n"
    log_file = LOG_DIR / "query_history.log"
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_line)

def process_batch_file(file_path: str, mode_choice: str) -> None:
    """
    处理批量文件，根据模式选择导出结果到新文件或修改原文件。
    
    参数:
        file_path: 文件路径
        mode_choice: 处理模式（"1"导出新文件，"2"修改原文件）
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