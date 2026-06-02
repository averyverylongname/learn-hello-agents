from typing import Any, Dict

from my_hello_agents.tools.base import Tool


class TextStatsTool(Tool):
    name = "text_stats"
    description = (
        "用于统计文本的字符数、非空白字符数、单词数和行数。"
        "Action Input 必须是 JSON，例如："
        "{\"text\": \"Hello Agent\"}"
    )

    def run(self, params: Dict[str, Any]) -> Any:
        text = params.get("text")

        if text is None:
            raise ValueError("缺少参数 text")

        total_chars = len(text)
        non_space_chars = len("".join(text.split()))
        words = len(text.split())
        lines = len(text.splitlines()) if text else 0

        return {
            "total_chars": total_chars,
            "non_space_chars": non_space_chars,
            "words": words,
            "lines": lines
        }