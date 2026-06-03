from my_hello_agents.core.llm import HelloAgentsLLM
from my_hello_agents.agents.react_agent import ReActAgent

from my_hello_agents.tools.registry import ToolRegistry
from my_hello_agents.tools.builtin.calculator import CalculatorTool
from my_hello_agents.tools.builtin.file_read import FileReadTool
from my_hello_agents.tools.builtin.file_search import FileSearchTool


def main():
    llm = HelloAgentsLLM()

    registry = ToolRegistry()
    registry.register(CalculatorTool())
    registry.register(FileReadTool(base_dir="."))
    registry.register(FileSearchTool(base_dir="."))

    agent = ReActAgent(
        llm=llm,
        tool_registry=registry,
        system_prompt=(
            "你是一名严谨的文件分析 Agent。"
            "当用户要求读取、总结、搜索文件内容时，必须调用文件工具，不能凭空回答。"
        ),
        max_steps=5,
        verbose=True
    )

    questions = [
        "请读取 examples/data/agent_intro.txt，并总结这个文件主要讲了什么。",
        "请在 examples/data/agent_intro.txt 中搜索 ReAct，并告诉我它在哪一行。",
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