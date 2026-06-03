class AgentError(Exception):
    """Agent 框架基础异常。"""
    pass


class LLMError(AgentError):
    """LLM 调用异常。"""
    pass


class ToolError(AgentError):
    """工具相关异常。"""
    pass


class ToolNotFoundError(ToolError):
    """工具不存在。"""
    pass


class ToolExecutionError(ToolError):
    """工具执行失败。"""
    pass


class ToolInputError(ToolError):
    """工具输入参数错误。"""
    pass