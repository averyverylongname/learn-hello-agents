from my_hello_agents.core.llm import HelloAgentsLLM
from my_hello_agents.agents.react_agent import ReActAgent
from my_hello_agents.tools.registry import ToolRegistry
from my_hello_agents.tools.builtin.calculator import CalculatorTool


def main():
    llm = HelloAgentsLLM()

    registry = ToolRegistry()
    registry.register(CalculatorTool())

    agent = ReActAgent(
        llm=llm,
        tool_registry=registry,
        system_prompt="你是一名严谨的 Agent，必须按照指定格式思考和调用工具。",
        verbose=True
    )

    question = "请计算 (12 + 8) * 3 的结果，并用一句话解释计算过程。"

    answer = agent.run(question)

    print("\n===== 最终答案 =====")
    print(answer)

    print("\n===== 执行轨迹 =====")
    for step in agent.get_trace():
        print(step)

if __name__ == "__main__":
    main()