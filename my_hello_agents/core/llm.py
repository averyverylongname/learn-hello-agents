from typing import List

from openai import OpenAI

from my_hello_agents.core.config import LLMConfig
from my_hello_agents.core.message import Message


class HelloAgentsLLM:
    def __init__(self, config: LLMConfig | None = None):
        self.config = config or LLMConfig()
        self.config.validate()

        self.client = OpenAI(
            api_key=self.config.api_key,
            base_url=self.config.base_url
        )

    def chat(self, messages: List[Message]) -> str:
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[message.to_dict() for message in messages],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )

        return response.choices[0].message.content