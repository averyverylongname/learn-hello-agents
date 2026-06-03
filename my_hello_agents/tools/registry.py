from typing import Dict, List

from my_hello_agents.tools.base import Tool
from my_hello_agents.core.exceptions import ToolNotFoundError


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        if tool.name in self._tools:
            raise ValueError(f"工具已存在：{tool.name}")

        self._tools[tool.name] = tool

    def get_tool(self, name: str) -> Tool:
        if name not in self._tools:
            raise ToolNotFoundError(f"工具不存在：{name}")

        return self._tools[name]

    def list_tools(self) -> List[Tool]:
        return list(self._tools.values())

    def get_tool_descriptions(self) -> str:
        return "\n".join(
            tool.to_prompt_description()
            for tool in self._tools.values()
        )