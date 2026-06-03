from my_hello_agents.core.llm import HelloAgentsLLM
from my_hello_agents.core.context import ContextManager
from my_hello_agents.agents.react_agent import ReActAgent

from my_hello_agents.rag.simple_rag import SimpleRAGIndex
from my_hello_agents.tools.registry import ToolRegistry
from my_hello_agents.tools.builtin.rag_search import RAGSearchTool


def main():
    # 1. 初始化 LLM
    llm = HelloAgentsLLM()

    # 2. 构建简单 RAG 索引
    rag_index = SimpleRAGIndex(
        base_dir=".",
        chunk_size=200,
        chunk_overlap=30
    )

    # 加载知识库目录
    rag_index.build_from_dir("examples/data/rag_docs")

    # 3. 注册工具
    registry = ToolRegistry()
    registry.register(RAGSearchTool(rag_index))

    # 4. 创建上下文管理器
    context_manager = ContextManager(
        max_history_messages=4,      # 最多保留最近 4 条历史消息
        max_message_chars=300,       # 每条历史消息最多 300 字
        max_scratchpad_chars=1200,   # scratchpad 最多 1200 字
        max_observation_chars=800    # 单次工具返回结果最多 800 字
    )

    # 5. 创建 ReActAgent
    agent = ReActAgent(
        llm=llm,
        tool_registry=registry,
        system_prompt=(
            "你是一名具备上下文管理能力的知识库问答 Agent。"
            "当用户询问 Agent、ReAct、工具调用、框架组成等知识时，"
            "必须先调用 rag_search 检索知识库，再基于检索结果回答。"
            "如果检索结果中没有依据，要明确说明没有检索到相关依据。"
        ),
        max_steps=5,
        verbose=True,
        context_manager=context_manager
    )

    # 6. 多轮测试问题
    questions = [
        "ReAct 是什么？",
        "它的执行过程是什么？",
        "它适合哪些任务？",
        "和普通聊天机器人相比，Agent 有什么区别？",
        "刚才我们主要讨论了什么？"
    ]

    # 7. 执行多轮对话
    for index, question in enumerate(questions, start=1):
        print(f"\n\n========== 第 {index} 轮 ==========")
        print("用户：", question)

        answer = agent.run(question)

        print("\n最终答案：")
        print(answer)

        print("\n当前进入历史中的消息数量：", len(agent.get_history()))

        print("\n本轮执行轨迹：")
        for step in agent.get_trace():
            print(step)


if __name__ == "__main__":
    main()