from pathlib import Path
from typing import Any, Dict, List

from my_hello_agents.tools.base import Tool


class FileSearchTool(Tool):
    name = "file_search"
    description = (
        "用于在本地文本文件中搜索关键词，并返回命中的行。"
        "Action Input 必须是 JSON，例如："
        "{\"path\": \"examples/data/agent_intro.txt\", \"keyword\": \"ReAct\"}"
    )

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir).resolve()

    def run(self, params: Dict[str, Any]) -> Any:
        path = params.get("path")
        keyword = params.get("keyword")

        if not path:
            raise ValueError("缺少参数 path")

        if not keyword:
            raise ValueError("缺少参数 keyword")

        file_path = (self.base_dir / path).resolve()

        if not self._is_safe_path(file_path):
            raise ValueError("不允许搜索 base_dir 之外的文件")

        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在：{path}")

        if not file_path.is_file():
            raise ValueError(f"不是普通文件：{path}")

        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            raise ValueError("文件不是 UTF-8 文本文件，暂不支持搜索")

        results: List[Dict[str, Any]] = []

        for index, line in enumerate(lines, start=1):
            if keyword.lower() in line.lower():
                results.append({
                    "line_number": index,
                    "line": line
                })

        if not results:
            return f"没有找到关键词：{keyword}"

        return results

    def _is_safe_path(self, file_path: Path) -> bool:
        try:
            file_path.relative_to(self.base_dir)
            return True
        except ValueError:
            return False