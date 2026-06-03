from pathlib import Path
from typing import Any, Dict

from my_hello_agents.tools.base import Tool


class FileReadTool(Tool):
    name = "file_read"
    description = (
        "用于读取本地文本文件内容。"
        "Action Input 必须是 JSON，例如："
        "{\"path\": \"examples/data/agent_intro.txt\"}。"
        "只适合读取 txt、md、py、json、csv 等文本文件。"
    )

    def __init__(self, base_dir: str = "."):
        self.base_dir = Path(base_dir).resolve()

    def run(self, params: Dict[str, Any]) -> Any:
        path = params.get("path")

        if not path:
            raise ValueError("缺少参数 path")

        file_path = (self.base_dir / path).resolve()

        if not self._is_safe_path(file_path):
            raise ValueError("不允许读取 base_dir 之外的文件")

        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在：{path}")

        if not file_path.is_file():
            raise ValueError(f"不是普通文件：{path}")

        try:
            return file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            raise ValueError("文件不是 UTF-8 文本文件，暂不支持读取")
    
    def _is_safe_path(self, file_path: Path) -> bool:
        try:
            file_path.relative_to(self.base_dir)
            return True
        except ValueError:
            return False