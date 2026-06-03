from typing import Any, Dict

from my_hello_agents.tools.base import Tool


class CalculatorTool(Tool):
    name = "calculator"
    description = "用于执行简单数学表达式计算。Action Input 必须是 JSON，例如：{\"expression\": \"1 + 2 * 3\"}"

    def run(self, params: Dict[str, Any]) -> Any:
        expression = params.get("expression")

        if not expression:
            raise ValueError("缺少参数 expression")

        allowed_chars = "0123456789+-*/(). %"

        if not all(char in allowed_chars for char in expression):
            raise ValueError("表达式包含不允许的字符")

        try:
            return eval(expression)
        except Exception as e:
            raise ValueError(f"表达式计算失败：{e}")