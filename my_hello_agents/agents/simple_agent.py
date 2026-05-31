from my_hello_agents.core.agent import Agent
from my_hello_agents.core.llm import HelloAgentsLLM


class SimpleAgent(Agent):
    def __init__(
        self,
        llm: HelloAgentsLLM,
        name: str = "SimpleAgent",
        system_prompt: str = "你是一个简洁、耐心的 AI 助手。"
    ):
        super().__init__(
            name=name,
            llm=llm,
            system_prompt=system_prompt
        )

    def run(self, user_input: str) -> str:
        self.add_user_message(user_input)

        response = self.llm.chat(self.get_history())

        self.add_assistant_message(response)

        return response