# ZellerDay 📅→📆

**通过蔡勒公式快速计算任意日期是星期几 | 优雅简洁的命令行工具**

---

## ✨ 项目简介

ZellerDay 是一个基于Python实现的日期计算工具，采用经典的[蔡勒公式](https://en.wikipedia.org/wiki/Zeller%27s_congruence)，只需输入任意合法日期，即可瞬间获取对应的星期信息。项目功能完善，代码简洁规范，适合作为教学案例。

```bash
示例输出：
请输入日期（如2025-02-24），或直接回车选择逐步输入：2025-02-24

2025年2月24日 是 星期一。

是否要继续计算其他日期？(y/n):
```

---

## 🚀 功能特性

- 📌 支持两种输入模式：单行日期格式 (`YYYY-MM-DD`) 或分步输入年月日
- 🛡️ 严格的日期有效性校验（包括闰年二月规则）
- ⚡ 支持批量日期文件处理
- 🔁 交互式循环查询模式
- 📚 100% 纯Python实现，零第三方依赖

---

## 💡 功能提示

- 当月份或日期为个位数时，此时输入的月份或日期会被自动补零，例如：2025-01-01会被自动修改为2025-01-01。

- 批量日期文件处理功能不只支持 txt 格式，只要是文本文件，并且日期可以按行读取，就可以处理。例如，.txt, .csv, .log 等文本格式的文件都可以。

- 批量日期文件内的日期需要每行一个日期进行排列，日期格式必须为 YYYY-MM-DD，日期之间使用换行符分隔。

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
git clone https://github.com/YifanHere/ZellerDay.git
cd ZellerDay
```

### 运行程序
```bash
python main.py
```

### 使用示例
```
欢迎使用 ZellerDay 星期计算器
该程序通过蔡勒公式计算任一日期对应的星期。
请输入日期，格式为 YYYY-MM-DD 或直接回车后按提示输入。

请输入日期（如2025-02-24），或直接回车选择逐步输入：2025-02-24

2025年2月24日 是 星期一。

是否要继续计算其他日期？(y/n): y

请输入日期（如2025-02-24），或直接回车选择逐步输入：2025-02-29
日期格式错误或日期无效，请使用 YYYY-MM-DD 格式。

请输入日期（如2025-02-24），或直接回车选择逐步输入：2025-2-28

2025年2月28日 是 星期五。

是否要继续计算其他日期？(y/n): n
感谢使用，再见！
```

---

## 🌱 扩展计划

- ✅ 支持批量日期文件处理
- ✅ 生成日期查询历史报告
- ✅ 支持更多常用日期格式及日期分隔符
- ⬜ 开发REST API接口
- ⬜ 添加GUI界面（Tkinter/PyQt）
- ......
---