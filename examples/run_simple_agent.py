from my_hello_agents.core.llm import HelloAgentsLLM
from my_hello_agents.agents.simple_agent import SimpleAgent


def main():
    llm = HelloAgentsLLM()

    agent = SimpleAgent(
        llm=llm,
        system_prompt="你是一名 Agent 开发老师，请用通俗易懂的方式回答问题。"
    )

    user_input = "请用一句话解释 Agent 和普通聊天机器人的区别。"

    response = agent.run(user_input)

    print("用户：", user_input)
    print("助手：", response)
    print("历史消息数量：", len(agent.get_history()))


if __name__ == "__main__":
    main()