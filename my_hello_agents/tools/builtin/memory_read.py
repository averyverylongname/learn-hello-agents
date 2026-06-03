from typing import Any, Dict

from my_hello_agents.memory.json_memory import JsonMemoryStore
from my_hello_agents.tools.base import Tool


class MemoryReadTool(Tool):
    name = "memory_read"
    description = (
        "用于读取所有长期记忆。"
        "Action Input 必须是 JSON，例如：{}"
    )

    def __init__(self, store: JsonMemoryStore):
        self.store = store

    def run(self, params: Dict[str, Any]) -> Any:
        return self.store.list_all()