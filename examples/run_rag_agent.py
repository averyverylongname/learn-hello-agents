from my_hello_agents.core.llm import HelloAgentsLLM
from my_hello_agents.agents.react_agent import ReActAgent

from my_hello_agents.rag.simple_rag import SimpleRAGIndex
from my_hello_agents.tools.registry import ToolRegistry
from my_hello_agents.tools.builtin.rag_search import RAGSearchTool


def main():
    llm = HelloAgentsLLM()

    rag_index = SimpleRAGIndex(
        base_dir=".",
        chunk_size=200,
        chunk_overlap=30
    )
    rag_index.build_from_dir("examples/data/rag_docs")

    registry = ToolRegistry()
    registry.register(RAGSearchTool(rag_index))

    agent = ReActAgent(
        llm=llm,
        tool_registry=registry,
        system_prompt=(
            "你是一名知识库问答 Agent。"
            "当用户询问 Agent、ReAct、工具调用、框架组成等知识时，"
            "必须先调用 rag_search 检索知识库，再基于检索结果回答。"
            "如果知识库没有相关内容，要明确说明没有检索到依据。"
        ),
        max_steps=5,
        verbose=True
    )

    questions = [
        "ReAct 是什么？它的执行过程是什么？",
        "一个基础 Agent 框架通常由哪些模块组成？",
        "Agent 和普通聊天机器人有什么区别？"
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