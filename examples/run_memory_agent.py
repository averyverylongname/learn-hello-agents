from my_hello_agents.core.llm import HelloAgentsLLM
from my_hello_agents.agents.react_agent import ReActAgent

from my_hello_agents.memory.json_memory import JsonMemoryStore
from my_hello_agents.tools.registry import ToolRegistry
from my_hello_agents.tools.builtin.memory_write import MemoryWriteTool
from my_hello_agents.tools.builtin.memory_read import MemoryReadTool
from my_hello_agents.tools.builtin.memory_search import MemorySearchTool


def main():
    llm = HelloAgentsLLM()

    memory_store = JsonMemoryStore("examples/data/memory.json")

    registry = ToolRegistry()
    registry.register(MemoryWriteTool(memory_store))
    registry.register(MemoryReadTool(memory_store))
    registry.register(MemorySearchTool(memory_store))

    agent = ReActAgent(
        llm=llm,
        tool_registry=registry,
        system_prompt=(
            "你是一名具备长期记忆能力的 Agent。"
            "当用户要求你记住某些信息时，必须调用 memory_write；"
            "当用户询问你记住了什么时，必须调用 memory_read 或 memory_search。"
        ),
        max_steps=5,
        verbose=True
    )

    questions = [
        "请记住：我正在围绕 Hello-Agents 项目学习 Agent 开发，目前已经完成到第七章的复刻开发。",
        "请搜索你记住的和 Hello-Agents 相关的信息。",
        "请告诉我你目前记住了哪些内容。"
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