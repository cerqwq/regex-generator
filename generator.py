"""
Regex Generator - AI正则表达式生成器
支持正则生成、解释、测试
"""

import json
import os
import re
from typing import Dict, List, Any
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class RegexGenerator:
    """
    AI正则表达式生成器
    支持：生成、解释、测试、优化
    """

    def __init__(self, model: str = "mimo-v2.5-pro", api_key: str = None, base_url: str = None):
        self.model = model
        if OPENAI_AVAILABLE:
            self.client = OpenAI(
                api_key=api_key or os.environ.get('OPENAI_API_KEY', ''),
                base_url=base_url or os.environ.get('OPENAI_BASE_URL', 'https://api.xiaomimimo.com/v1')
            )
        else:
            self.client = None

    def generate(self, description: str, examples: List[str] = None) -> Dict:
        """生成正则表达式"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        examples_text = "\n".join(f"- {e}" for e in (examples or []))

        prompt = f"""请根据以下描述生成正则表达式：

描述：{description}
{f'示例匹配：{examples_text}' if examples_text else ''}

请返回JSON格式：
{{
    "regex": "正则表达式",
    "explanation": "解释",
    "examples": ["匹配示例1", "匹配示例2"],
    "non_examples": ["不匹配示例1"]
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re as re_module
            json_match = re_module.search(r'\{.*\}', content, re_module.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"regex": content}

    def explain(self, regex: str) -> str:
        """解释正则表达式"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请详细解释以下正则表达式：

{regex}

要求：
1. 逐部分解释
2. 说明匹配规则
3. 给出匹配示例"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        return response.choices[0].message.content

    def test(self, regex: str, test_strings: List[str]) -> Dict:
        """测试正则表达式"""
        results = {"matches": [], "non_matches": []}

        try:
            pattern = re.compile(regex)
            for s in test_strings:
                if pattern.search(s):
                    results["matches"].append(s)
                else:
                    results["non_matches"].append(s)
        except re.error as e:
            return {"error": f"Invalid regex: {e}"}

        return results

    def optimize(self, regex: str) -> Dict:
        """优化正则表达式"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        prompt = f"""请优化以下正则表达式：

{regex}

请返回JSON格式：
{{
    "optimized": "优化后的正则",
    "issues": ["问题1", "问题2"],
    "improvements": ["改进1", "改进2"],
    "performance": "性能说明"
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re as re_module
            json_match = re_module.search(r'\{.*\}', content, re_module.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"optimization": content}

    def from_examples(self, positive: List[str], negative: List[str] = None) -> Dict:
        """从示例生成正则"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        positive_text = "\n".join(f"+ {p}" for p in positive)
        negative_text = "\n".join(f"- {n}" for n in (negative or []))

        prompt = f"""请根据以下示例生成正则表达式：

应该匹配：
{positive_text}

{f'不应该匹配：{negative_text}' if negative_text else ''}

请返回JSON格式：
{{
    "regex": "正则表达式",
    "explanation": "解释",
    "accuracy": "准确率说明"
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )

        try:
            content = response.choices[0].message.content
            import re as re_module
            json_match = re_module.search(r'\{.*\}', content, re_module.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"regex": content}

    def extract_patterns(self, text: str, pattern_type: str = "email") -> List[str]:
        """提取文本中的模式"""
        patterns = {
            "email": r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            "phone": r'1[3-9]\d{9}',
            "url": r'https?://[^\s]+',
            "ip": r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',
            "date": r'\d{4}[-/]\d{1,2}[-/]\d{1,2}',
        }

        pattern = patterns.get(pattern_type)
        if not pattern:
            return []

        return re.findall(pattern, text)


def create_generator(**kwargs) -> RegexGenerator:
    """创建正则生成器"""
    return RegexGenerator(**kwargs)


if __name__ == "__main__":
    generator = create_generator()

    print("Regex Generator")
    print()

    # 测试
    result = generator.generate("匹配中国手机号码", ["13812345678", "15900001111"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
