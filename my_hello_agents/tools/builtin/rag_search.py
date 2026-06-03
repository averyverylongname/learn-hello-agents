from typing import Any, Dict

from my_hello_agents.rag.simple_rag import SimpleRAGIndex
from my_hello_agents.tools.base import Tool


class RAGSearchTool(Tool):
    name = "rag_search"
    description = (
        "用于在知识库文档中检索与问题相关的文本片段。"
        "Action Input 必须是 JSON，例如："
        "{\"query\": \"ReAct 是什么\", \"top_k\": 3}"
    )

    def __init__(self, index: SimpleRAGIndex):
        self.index = index

    def run(self, params: Dict[str, Any]) -> Any:
        query = params.get("query")
        top_k = params.get("top_k", 3)

        if not query:
            raise ValueError("缺少参数 query")

        results = self.index.search(query=query, top_k=int(top_k))

        if not results:
            return "没有检索到相关文档片段。"

        return results