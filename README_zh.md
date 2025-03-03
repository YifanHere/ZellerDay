# ZellerDay 📅→📆

**通过蔡勒公式快速计算任意日期是星期几 | 优雅简洁的命令行工具**

这个项目是我多年以前学习Python时练手的项目，经过这个项目的编写，我入门了Python，在最近的学习中我再次接触到蔡勒公式。所以上传至GitHub，我对原始代码作出了扩展并进一步规范化，旨在为更多人的学习提供参考。

---

## ✨ 项目简介

ZellerDay 是一个基于Python实现的，采用经典的[蔡勒公式（Zeller's Congruence）](https://en.wikipedia.org/wiki/Zeller%27s_congruence)来计算任一日期对应星期的工具。
通过内置的日期解析功能，程序支持处理多种常见日期格式，并在遇到输入歧义时通过交互提示用户选择相应解析方式。
项目功能完善，代码简洁规范，适合作为教学或自学案例。

---

## 🚀 功能特性
- ✔️ **高度计算兼容性**：支持使用蔡勒公式计算**任一日期**（除去不存在的日期）对应的星期，**兼容公元前及公元后的日期（负年份）**
- 🔢 **高度输入兼容性**：当输入存在歧义（例如数值都小于等于31时），程序会通过交互提示用户选择正确的解析方式
- 📊 **历法转换处理**：自动处理公历（格里高利历）和儒略历的转换，对于1582年10月4日及之前的日期使用儒略历公式，对于1582年10月15日及之后的日期使用公历公式
- 📌 **支持两种输入模式**：可一次性输入完整日期或分步输入年月日
- ⚡ **支持批量日期文件处理**：内置批处理功能，可以读取文本文件中的每行日期，进行计算，并根据用户选择导出为新文件或修改原文件
- 🔁 **日志记录**：所有日期查询结果均记录在 data/logs/query_history.log 文件中，记录格式为 "时间戳 - 查询 -> 结果"
- 🌐 **多语言支持**：自动检测用户语言环境并提供相应的界面语言（英文或中文），也可通过命令行参数手动指定语言
- 📚 **零第三方依赖**：100% 纯Python实现
- 🛡️ **多格式日期输入**：程序支持多种日期格式，包括但不限于：
  - YYYY-MM-DD
  - YYYY/MM/DD
  - YYYY.MM.DD
  - DD-MM-YYYY
  - DD/MM/YYYY
  - DD.MM.YYYY
  - 以及其他格式

---

## 📂 项目结构

```
ZellerDay/
├── data/                  # 数据目录
│   └── logs/              # 日志存储目录
├── tests/                 # 测试目录
│   ├── __init__.py
│   └── test_zeller_day.py # 单元测试文件
├── zeller_day/            # 主要源代码目录
│   ├── __init__.py
│   ├── cli.py             # 命令行界面模块
│   ├── core.py            # 核心计算模块（蔡勒公式实现）
│   ├── date_utils.py      # 日期处理工具
│   ├── io_utils.py        # 输入输出工具
│   └── language.py        # 语言配置模块（多语言支持）
├── .gitignore
├── LICENSE.md
├── main.py                # 程序入口
├── README.md
└── requirements.txt
```

---

## 💡 功能提示

- 当月份或日期为个位数时，此时输入的月份或日期会被自动补零，例如：233-1-1会被自动修改为0233-01-01
- 公元前日期处理：
  - 程序支持计算公元前日期，输入负年份即可，例如 -1414/5/14 表示公元前1414年5月14日
  - 公元前日期会在控制台显示天文转换信息，例如 "[DEBUG] 天文转换: 原始年份 -1414 转换为年 -1413"

- 批量日期文件处理功能不只支持 txt 格式，只要是文本文件，并且日期可以按行读取，就可以处理。例如，.txt, .csv, .log 等文本格式的文件都可以

- 批量处理模式：  
  - 程序支持批量处理日期文件，可以通过在命令行中，使用以下命令来运行批量处理功能：
    ```bash
    python main.py batch <文件路径> <处理模式>
    ```
  - 处理模式：
    - 1 - 导出到新文件（生成 原文件名_result.扩展名）
    - 2 - 修改原文件

- 批量日期文件内的日期需要每行一个日期进行排列，日期格式必须为 YYYY-MM-DD，YYYY/MM/DD 或 YYYY.MM.DD 等支持的格式，日期之间使用换行符分隔
  - 例如，一个符合要求的批量日期文件内容如下：
    >```bash
    >2025-01-01
    >2025-02-14
    >2025-03-15
    >2025-04-01
    >2025-05-01
    >```

---

## 📦 快速开始

### 环境要求
- Python 3.x

### 安装步骤
```bash
# 克隆仓库
git clone https://github.com/YifanHere/ZellerDay.git
cd ZellerDay

# 无需安装额外依赖
```

### 运行程序
```bash
# 交互模式
python main.py

# 指定语言（中文）
python main.py --lang=zh

# 指定语言（英文）
python main.py --lang=en

# 批量处理模式
python main.py batch <文件路径> <处理模式>
# 例如：python main.py batch dates.txt 1

# 批量处理模式并指定语言
python main.py --lang=en batch <文件路径> <处理模式>
```

### 使用示例

**英文界面(默认)**
```
Welcome to ZellerDay Weekday Calculator
This program calculates the weekday for any date using Zeller's formula.

Please enter a date (e.g. 2025-02-24), or press Enter for step-by-step input: 2025-2-24

2025-02-24 is Monday。

Do you want to calculate another date? (Y/N/Enter):
Please enter the year (e.g. 2025 or 3 or -123): 5201
Please enter the month (e.g. 2): 3
Please enter the day (e.g. 24): 14

5201-03-14 is Wednesday。

Do you want to calculate another date? (Y/N/Enter): -1414/5/14
[DEBUG] Astronomical conversion: Original year -1414 converted to year -1413

-1414-05-14 is Thursday。

Do you want to calculate another date? (Y/N/Enter): n
Thank you for using ZellerDay, goodbye!
```
**中文界面（使用 --lang=zh 参数）**
```
欢迎使用 ZellerDay 星期计算器
该程序通过蔡勒公式计算任一日期对应星期。

请输入日期（如2025-02-24），或直接回车选择逐步输入：2025-2-24

2025年02月24日 是 星期一。

是否要继续计算其他日期？(Y/N/Enter):
请输入年份（例如2025 或 3 或 -123）：5201
请输入月份（例如2）：3
请输入日期（例如24）：14

5201年03月14日 是 星期三。

是否要继续计算其他日期？(Y/N/Enter): -1414/5/14
[DEBUG] 天文转换: 原始年份 -1414 转换为年 -1413

-1414年05月14日 是 星期四。

是否要继续计算其他日期？(Y/N/Enter): n
感谢使用，再见！
```

---

## 🧪 运行测试

项目包含完整的单元测试，可以通过以下命令运行测试：

```bash
# 在项目根目录下运行
python -m unittest discover tests
```

测试覆盖了核心计算功能、日期验证和解析功能、星期映射功能等关键部分。

---

## 🔧 开发者指南

### 代码结构

- **core.py**: 包含蔡勒公式的实现和星期映射功能
- **date_utils.py**: 包含日期验证、解析和格式化功能
- **io_utils.py**: 包含日志记录和批量文件处理功能
- **cli.py**: 包含命令行界面和用户交互功能
- **language.py**: 包含多语言支持、语言检测和文本本地化功能

### 贡献指南

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 打开一个 Pull Request

---

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE.md](LICENSE.md) 文件
