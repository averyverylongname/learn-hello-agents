from my_hello_agents.core.llm import HelloAgentsLLM
from my_hello_agents.agents.react_agent import ReActAgent

from my_hello_agents.tools.registry import ToolRegistry
from my_hello_agents.tools.builtin.calculator import CalculatorTool
from my_hello_agents.tools.builtin.file_read import FileReadTool


def main():
    llm = HelloAgentsLLM()

    registry = ToolRegistry()
    registry.register(CalculatorTool())
    registry.register(FileReadTool(base_dir="."))

    agent = ReActAgent(
        llm=llm,
        tool_registry=registry,
        system_prompt=(
            "你是一名严谨的 Agent。"
            "如果工具调用失败，需要根据 Observation 中的错误信息进行修正，"
            "或者向用户说明失败原因。"
        ),
        max_steps=5,
        verbose=True
    )

    questions = [
        "请计算 1 + 2 * 3。",
        "请读取一个不存在的文件 examples/data/not_exists.txt，并告诉我内容。",
        "请计算 abc + 1。"
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