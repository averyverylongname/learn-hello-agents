from abc import ABC, abstractmethod
from typing import List

from my_hello_agents.core.llm import HelloAgentsLLM
from my_hello_agents.core.message import (
    Message,
    system_message,
    user_message,
    assistant_message,
)


class Agent(ABC):
    def __init__(
        self,
        name: str,
        llm: HelloAgentsLLM,
        system_prompt: str = "你是一个有帮助的 AI 助手。"
    ):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt
        self.history: List[Message] = []

        self.add_message(system_message(system_prompt))

    def add_message(self, message: Message):
        self.history.append(message)

    def add_user_message(self, content: str):
        self.add_message(user_message(content))

    def add_assistant_message(self, content: str):
        self.add_message(assistant_message(content))

    def get_history(self) -> List[Message]:
        return self.history

    def clear_history(self):
        self.history = []
        self.add_message(system_message(self.system_prompt))

    @abstractmethod
    def run(self, user_input: str) -> str:
        pass