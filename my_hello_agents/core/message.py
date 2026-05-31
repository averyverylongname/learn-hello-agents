from dataclasses import dataclass
from typing import Dict


@dataclass
class Message:
    role: str
    content: str

    def to_dict(self) -> Dict[str, str]:
        return {
            "role": self.role,
            "content": self.content
        }


def system_message(content: str) -> Message:
    return Message(role="system", content=content)


def user_message(content: str) -> Message:
    return Message(role="user", content=content)


def assistant_message(content: str) -> Message:
    return Message(role="assistant", content=content)