from my_hello_agents.core.llm import HelloAgentsLLM
from my_hello_agents.agents.react_agent import ReActAgent

from my_hello_agents.tools.registry import ToolRegistry
from my_hello_agents.tools.builtin.calculator import CalculatorTool
from my_hello_agents.tools.builtin.time_tool import TimeTool
from my_hello_agents.tools.builtin.text_stats import TextStatsTool


def main():
    llm = HelloAgentsLLM()

    registry = ToolRegistry()
    registry.register(CalculatorTool())
    registry.register(TimeTool())
    registry.register(TextStatsTool())

    agent = ReActAgent(
        llm=llm,
        tool_registry=registry,
        system_prompt="你是一名严谨的多工具 Agent，遇到计算、时间、文本统计问题必须调用工具。",
        max_steps=5,
        verbose=True
    )

    questions = [
        "请计算 (18 + 6) / 3 的结果。",
        "请告诉我 Asia/Singapore 时区现在的时间。",
        "请统计这句话的字符数和单词数：Hello Agent Framework",
    ]

    for index, question in enumerate(questions, start=1):
        print(f"\n\n========== 问题 {index} ==========")
        print("用户：", question)

        answer = agent.run(question)

        print("\n最终答案：")
        print(answer)

        print("\n执行轨迹：")
        for step in agent.get_trace():
            print(step)


if __name__ == "__main__":
    main()