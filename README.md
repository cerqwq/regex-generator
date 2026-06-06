# 🔤 Regex Generator

AI正则表达式生成器，支持正则生成、解释、测试。

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
  <img src="https://img.shields.io/badge/OpenAI-API-green?logo=openai" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

## ✨ 特性

- 🔤 正则表达式生成
- 📖 正则表达式解释
- ✅ 正则表达式测试
- ⚡ 正则表达式优化
- 📝 从示例生成
- 🔍 模式提取

## 🚀 快速开始

```bash
pip install openai

python generator.py
```

## 📖 使用

```python
from regex_generator import create_generator

generator = create_generator()

# 生成正则
result = generator.generate("匹配中国手机号码", ["13812345678"])

# 解释正则
explanation = generator.explain(r"1[3-9]\d{9}")

# 测试正则
test_result = generator.test(r"\d+", ["abc123", "xyz", "456"])

# 优化正则
optimized = generator.optimize(r"[0-9][0-9][0-9]")

# 从示例生成
result = generator.from_examples(["test@email.com"], ["not-email"])

# 提取模式
emails = generator.extract_patterns(text, "email")
```

## 📁 项目结构

```
regex-generator/
├── generator.py   # 正则生成器核心
└── README.md
```

## 📄 许可证

MIT License
