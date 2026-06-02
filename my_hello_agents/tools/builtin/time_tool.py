from datetime import datetime
from typing import Any, Dict
from zoneinfo import ZoneInfo

from my_hello_agents.tools.base import Tool


class TimeTool(Tool):
    name = "time_tool"
    description = (
        "用于获取指定时区的当前时间。"
        "Action Input 必须是 JSON，例如："
        "{\"timezone\": \"Asia/Shanghai\"}。"
        "如果用户没有指定时区，可以使用 Asia/Shanghai。"
    )

    def run(self, params: Dict[str, Any]) -> Any:
        timezone = params.get("timezone", "Asia/Shanghai")

        try:
            now = datetime.now(ZoneInfo(timezone))
        except Exception:
            raise ValueError(f"无效的时区：{timezone}")

        return now.strftime("%Y-%m-%d %H:%M:%S %Z")