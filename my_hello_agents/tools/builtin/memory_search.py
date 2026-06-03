from typing import Any, Dict

from my_hello_agents.memory.json_memory import JsonMemoryStore
from my_hello_agents.tools.base import Tool


class MemorySearchTool(Tool):
    name = "memory_search"
    description = (
        "用于按关键词搜索长期记忆。"
        "Action Input 必须是 JSON，例如："
        "{\"keyword\": \"Hello-Agents\"}"
    )

    def __init__(self, store: JsonMemoryStore):
        self.store = store

    def run(self, params: Dict[str, Any]) -> Any:
        keyword = params.get("keyword")

        if not keyword:
            raise ValueError("缺少参数 keyword")

        return self.store.search(keyword)