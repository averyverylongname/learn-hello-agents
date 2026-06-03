from typing import List

from my_hello_agents.core.message import Message


class ContextManager:
    def __init__(
        self,
        max_history_messages: int = 8,
        max_message_chars: int = 1000,
        max_scratchpad_chars: int = 3000,
        max_observation_chars: int = 1500
    ):
        self.max_history_messages = max_history_messages
        self.max_message_chars = max_message_chars
        self.max_scratchpad_chars = max_scratchpad_chars
        self.max_observation_chars = max_observation_chars

    def format_history(self, history: List[Message]) -> str:
        non_system_messages = [
            message for message in history
            if message.role != "system"
        ]

        recent_messages = non_system_messages[-self.max_history_messages:]

        if not recent_messages:
            return "暂无历史对话。"

        lines = []

        for message in recent_messages:
            content = self.truncate_text(
                message.content,
                self.max_message_chars
            )

            if message.role == "user":
                lines.append(f"用户：{content}")
            elif message.role == "assistant":
                lines.append(f"助手：{content}")
            else:
                lines.append(f"{message.role}：{content}")

        return "\n".join(lines)

    def trim_scratchpad(self, scratchpad: str) -> str:
        return self.truncate_text(
            scratchpad,
            self.max_scratchpad_chars,
            keep_tail=True
        )

    def trim_observation(self, observation: str) -> str:
        return self.truncate_text(
            observation,
            self.max_observation_chars
        )

    def truncate_text(
        self,
        text: str,
        max_chars: int,
        keep_tail: bool = False
    ) -> str:
        if text is None:
            return ""

        text = str(text)

        if len(text) <= max_chars:
            return text

        if keep_tail:
            return (
                f"[前文过长，已省略，只保留最后 {max_chars} 字]\n"
                + text[-max_chars:]
            )

        return text[:max_chars] + f"\n[内容过长，已截断，原长度 {len(text)} 字]"