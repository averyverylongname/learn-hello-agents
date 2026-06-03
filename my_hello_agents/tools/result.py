from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class ToolResult:
    success: bool
    data: Any = None
    error: str | None = None
    metadata: Dict[str, Any] | None = None

    @classmethod
    def ok(cls, data: Any = None, metadata: Dict[str, Any] | None = None):
        return cls(
            success=True,
            data=data,
            error=None,
            metadata=metadata or {}
        )

    @classmethod
    def fail(cls, error: str, metadata: Dict[str, Any] | None = None):
        return cls(
            success=False,
            data=None,
            error=error,
            metadata=metadata or {}
        )

    def to_observation_text(self) -> str:
        if self.success:
            return f"工具执行成功，结果：{self.data}"

        return f"工具执行失败，错误信息：{self.error}"