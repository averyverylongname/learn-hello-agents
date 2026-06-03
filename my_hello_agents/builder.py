from my_hello_agents.core.llm import HelloAgentsLLM
from my_hello_agents.core.context import ContextManager
from my_hello_agents.agents.react_agent import ReActAgent

from my_hello_agents.tools.registry import ToolRegistry

from my_hello_agents.tools.builtin.calculator import CalculatorTool
from my_hello_agents.tools.builtin.time_tool import TimeTool
from my_hello_agents.tools.builtin.text_stats import TextStatsTool
from my_hello_agents.tools.builtin.file_read import FileReadTool
from my_hello_agents.tools.builtin.file_search import FileSearchTool

from my_hello_agents.memory.json_memory import JsonMemoryStore
from my_hello_agents.tools.builtin.memory_write import MemoryWriteTool
from my_hello_agents.tools.builtin.memory_read import MemoryReadTool
from my_hello_agents.tools.builtin.memory_search import MemorySearchTool

from my_hello_agents.rag.simple_rag import SimpleRAGIndex
from my_hello_agents.tools.builtin.rag_search import RAGSearchTool


def build_basic_registry(base_dir: str = ".") -> ToolRegistry:
    """
    构建基础工具注册中心：
    calculator、time_tool、text_stats、file_read、file_search
    """
    registry = ToolRegistry()

    registry.register(CalculatorTool())
    registry.register(TimeTool())
    registry.register(TextStatsTool())
    registry.register(FileReadTool(base_dir=base_dir))
    registry.register(FileSearchTool(base_dir=base_dir))

    return registry


def add_memory_tools(
    registry: ToolRegistry,
    memory_path: str = "examples/data/memory.json"
) -> ToolRegistry:
    """
    给已有 registry 增加 Memory 工具。
    """
    memory_store = JsonMemoryStore(memory_path)

    registry.register(MemoryWriteTool(memory_store))
    registry.register(MemoryReadTool(memory_store))
    registry.register(MemorySearchTool(memory_store))

    return registry


def add_rag_tool(
    registry: ToolRegistry,
    rag_dir: str = "examples/data/rag_docs",
    base_dir: str = ".",
    chunk_size: int = 200,
    chunk_overlap: int = 30
) -> ToolRegistry:
    """
    给已有 registry 增加 RAG 检索工具。
    """
    rag_index = SimpleRAGIndex(
        base_dir=base_dir,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    rag_index.build_from_dir(rag_dir)

    registry.register(RAGSearchTool(rag_index))

    return registry


def build_full_registry(
    base_dir: str = ".",
    memory_path: str = "examples/data/memory.json",
    rag_dir: str = "examples/data/rag_docs"
) -> ToolRegistry:
    """
    构建完整工具注册中心：
    基础工具 + Memory 工具 + RAG 工具
    """
    registry = build_basic_registry(base_dir=base_dir)

    add_memory_tools(
        registry=registry,
        memory_path=memory_path
    )

    add_rag_tool(
        registry=registry,
        rag_dir=rag_dir,
        base_dir=base_dir
    )

    return registry


def build_default_context_manager() -> ContextManager:
    """
    构建默认上下文管理器。
    """
    return ContextManager(
        max_history_messages=8,
        max_message_chars=800,
        max_scratchpad_chars=3000,
        max_observation_chars=1500
    )


def build_full_react_agent(
    verbose: bool = True,
    base_dir: str = ".",
    memory_path: str = "examples/data/memory.json",
    rag_dir: str = "examples/data/rag_docs"
) -> ReActAgent:
    """
    构建一个完整能力版 ReActAgent。
    """
    llm = HelloAgentsLLM()

    registry = build_full_registry(
        base_dir=base_dir,
        memory_path=memory_path,
        rag_dir=rag_dir
    )

    context_manager = build_default_context_manager()

    agent = ReActAgent(
        llm=llm,
        tool_registry=registry,
        system_prompt=(
            "你是一名具备工具调用、文件读取、长期记忆和知识库检索能力的 Agent。"
            "当问题需要计算、时间、文本统计、文件读取、记忆或知识库检索时，"
            "必须优先调用合适的工具，不要凭空编造。"
            "如果工具返回错误，要根据 Observation 说明失败原因或尝试修正。"
        ),
        max_steps=6,
        verbose=verbose,
        context_manager=context_manager
    )

    return agent