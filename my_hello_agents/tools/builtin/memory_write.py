from typing import Any, Dict

from my_hello_agents.memory.json_memory import JsonMemoryStore
from my_hello_agents.tools.base import Tool


class MemoryWriteTool(Tool):
    name = "memory_write"
    description = (
        "用于写入一条长期记忆。"
        "Action Input 必须是 JSON，例如："
        "{\"content\": \"用户正在学习 Hello-Agents 第七章\", \"metadata\": {\"type\": \"learning\"}}"
    )

    def __init__(self, store: JsonMemoryStore):
        self.store = store

    def run(self, params: Dict[str, Any]) -> Any:
        content = params.get("content")
        metadata = params.get("metadata", {})

        if not content:
            raise ValueError("缺少参数 content")

        return self.store.add(content=content, metadata=metadata)