#!/usr/bin/env python3
"""
ZellerDay单元测试
"""

import unittest
import sys
import os

from zeller_day.core import calculate_weekday, map_weekday
from zeller_day.date_utils import validate_date_input, is_valid_date

class TestZellerDay(unittest.TestCase):
    """ZellerDay测试类"""
    
    def test_calculate_weekday(self):
        """测试星期计算功能"""
        # 测试2000-01-01，星期六
        self.assertEqual(calculate_weekday(2000, 1, 1), 0)
        # 测试2025-02-24，预期星期一 (返回值为2)
        self.assertEqual(calculate_weekday(2025, 2, 24), 2)
        # 测试2020-02-29，预期星期六 (返回值为0)
        self.assertEqual(calculate_weekday(2020, 2, 29), 0)
    
    def test_validate_date_input(self):
        """测试日期验证和解析功能"""
        # 测试多种正确格式
        self.assertEqual(validate_date_input("2025-02-24"), (2025, 2, 24))
        self.assertEqual(validate_date_input("2025/02/24"), (2025, 2, 24))
        self.assertEqual(validate_date_input("2025.2.24"), (2025, 2, 24))
        # 测试公元前日期
        self.assertEqual(validate_date_input("-1-1-1"), (-1, 1, 1))
        self.assertEqual(validate_date_input("-1.1.1"), (-1, 1, 1))
        # 测试无歧义数字相同的情况，如 "1-1-1"
        self.assertEqual(validate_date_input("1-1-1"), (1, 1, 1))
    
    def test_is_valid_date(self):
        """测试日期合法性验证功能"""
        # 测试有效日期
        self.assertTrue(is_valid_date(2020, 2, 29))  # 闰年
        self.assertTrue(is_valid_date(-1, 2, 28))    # 公元前
        # 测试无效日期
        self.assertFalse(is_valid_date(2021, 2, 29))  # 非闰年2月29日
        self.assertFalse(is_valid_date(2021, 4, 31))  # 4月没有31日
        self.assertFalse(is_valid_date(2021, 13, 1))  # 无效月份
    
    def test_map_weekday(self):
        """测试星期映射功能"""
        self.assertEqual(map_weekday(0), "星期六")
        self.assertEqual(map_weekday(1), "星期日")
        self.assertEqual(map_weekday(2), "星期一")
        self.assertEqual(map_weekday(6), "星期五")

if __name__ == "__main__":
    unittest.main()