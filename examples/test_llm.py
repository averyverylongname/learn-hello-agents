from my_hello_agents.core.llm import HelloAgentsLLM
from my_hello_agents.core.message import system_message, user_message


llm = HelloAgentsLLM()

messages = [
    system_message("你是一个简洁、耐心的 Agent 开发老师。"),
    user_message("请用一句话解释什么是 Agent。")
]

response = llm.chat(messages)

print(response)