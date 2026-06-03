from abc import ABC, abstractmethod
from typing import Any, Dict

from my_hello_agents.tools.result import ToolResult


class Tool(ABC):
    name: str
    description: str

    @abstractmethod
    def run(self, params: Dict[str, Any]) -> Any:
        pass

    def safe_run(self, params: Dict[str, Any]) -> ToolResult:
        try:
            result = self.run(params)
            return ToolResult.ok(
                data=result,
                metadata={
                    "tool_name": self.name
                }
            )
        except Exception as e:
            return ToolResult.fail(
                error=str(e),
                metadata={
                    "tool_name": self.name,
                    "error_type": e.__class__.__name__
                }
            )

    def to_prompt_description(self) -> str:
        return f"{self.name}: {self.description}"