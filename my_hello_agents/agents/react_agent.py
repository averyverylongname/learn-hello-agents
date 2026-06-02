import json
import re
import ast
from typing import Any, Dict, Optional, Tuple

from my_hello_agents.core.agent import Agent
from my_hello_agents.core.llm import HelloAgentsLLM
from my_hello_agents.core.message import system_message, user_message
from my_hello_agents.tools.registry import ToolRegistry
from my_hello_agents.core.trace import TraceStep


class ReActAgent(Agent):
    def __init__(
        self,
        llm: HelloAgentsLLM,
        tool_registry: ToolRegistry,
        name: str = "ReActAgent",
        system_prompt: str = "你是一个可以通过思考和调用工具解决问题的智能体。",
        max_steps: int = 5,
        verbose: bool = True
    ):
        super().__init__(
            name=name,
            llm=llm,
            system_prompt=system_prompt
        )
        self.tool_registry = tool_registry
        self.max_steps = max_steps
        self.verbose = verbose
        self.trace_steps: list[TraceStep] = []

    def run(self, user_input: str) -> str:
        self.add_user_message(user_input)
        self.trace_steps = []

        scratchpad = ""

        for step in range(self.max_steps):
            conversation_history = self._format_conversation_history()
            prompt = self._build_prompt(
                conversation_history=conversation_history,
                scratchpad=scratchpad
            )

            llm_output = self.llm.chat([
                system_message(self.system_prompt),
                user_message(prompt)
            ])

            self._log(f"\n===== 第 {step + 1} 轮模型输出 =====")
            self._log(llm_output)

            thought = self._parse_thought(llm_output)
            final_answer = self._parse_final_answer(llm_output)

            if final_answer:
                self.trace_steps.append(
                    TraceStep(
                        step=step + 1,
                        thought=thought,
                        final_answer=final_answer,
                        raw_output=llm_output
                    )
                )
                self.add_assistant_message(final_answer)
                return final_answer

            action, action_input, parse_error = self._parse_action(llm_output)

            if not action:
                error_msg = parse_error or "未解析到 Action"
                self.trace_steps.append(
                    TraceStep(
                        step=step + 1,
                        thought=thought,
                        raw_output=llm_output,
                        error=error_msg
                    )
                )

                scratchpad += (
                    f"\n{llm_output}\n"
                    f"Observation: 模型输出格式错误：{error_msg}。请严格按照规定格式输出。\n"
                )
                continue

            try:
                tool = self.tool_registry.get_tool(action)
                observation = tool.run(action_input)
                error_msg = None
            except Exception as e:
                observation = f"工具调用失败：{e}"
                error_msg = str(e)

            self.trace_steps.append(
                TraceStep(
                    step=step + 1,
                    thought=thought,
                    action=action,
                    action_input=action_input,
                    observation=str(observation),
                    raw_output=llm_output,
                    error=error_msg
                )
            )

            scratchpad += (
                f"\n{llm_output}\n"
                f"Observation: {observation}\n"
            )

        fallback = "达到最大推理轮数，仍未得到最终答案。"
        self.add_assistant_message(fallback)
        return fallback

    def _build_prompt(self, conversation_history: str, scratchpad: str) -> str:
        tool_descriptions = self.tool_registry.get_tool_descriptions()

        return f"""
            你需要使用 ReAct 方式解决问题。

            你可以使用以下工具：
            {tool_descriptions}

            你必须严格使用以下两种格式之一。

            如果需要调用工具，请输出：
            Thought: 你的思考
            Action: 工具名称
            Action Input: JSON格式参数

            如果已经知道最终答案，请输出：
            Thought: 你的思考
            Final Answer: 最终答案

            规则：
            1. 每次只能调用一个工具。
            2. Action 必须是工具列表中的名称。
            3. Action Input 必须是合法 JSON 对象。
            4. 不要输出 Markdown 代码块。
            5. 不要编造工具执行结果，工具结果只能来自 Observation。
            6. 回答时要结合对话历史理解用户当前问题。
            7. 如果问题可以通过已有工具更准确地解决，应优先调用工具，不要直接猜测。
            8. 涉及数学计算、当前时间、文本统计的问题，必须调用对应工具。
            9. 当用户要求读取、总结、分析文件内容时，必须优先调用 file_read。
            10. 当用户要求查找某个关键词、定位文本位置时，必须优先调用 file_search。

            对话历史：
            {conversation_history}

            当前任务的中间推理过程：
            {scratchpad}

            请继续：
            """.strip()

    def _parse_final_answer(self, text: str) -> Optional[str]:
        match = re.search(r"Final Answer\s*:\s*(.*)", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def _parse_action(self, text: str):
        action_match = re.search(r"Action\s*:\s*([a-zA-Z0-9_\-]+)", text)
        input_match = re.search(r"Action Input\s*:\s*(.*)", text, re.DOTALL)

        if not action_match:
            return None, {}, "未找到 Action"

        if not input_match:
            return None, {}, "未找到 Action Input"

        action = action_match.group(1).strip()
        action_input_text = input_match.group(1).strip()

        # 去掉模型可能输出的 Markdown 代码块
        action_input_text = self._clean_action_input_text(action_input_text)

        try:
            action_input = json.loads(action_input_text)
            return action, action_input, None
        except json.JSONDecodeError:
            pass

        try:
            action_input = ast.literal_eval(action_input_text)
            if isinstance(action_input, dict):
                return action, action_input, None
        except Exception:
            pass

        # 兜底：如果 calculator 的参数不是 JSON，而是普通表达式，就自动包装
        if action == "calculator":
            return action, {"expression": action_input_text}, None

        return action, {"input": action_input_text}, None

    def _clean_action_input_text(self, text: str) -> str:
        text = text.strip()

        if text.startswith("```"):
            text = re.sub(r"^```[a-zA-Z]*", "", text)
            text = re.sub(r"```$", "", text).strip()

        stop_words = ["\nObservation:", "\nThought:", "\nFinal Answer:"]
        for stop_word in stop_words:
            if stop_word in text:
                text = text.split(stop_word)[0].strip()

        return text

    def _parse_thought(self, text: str) -> str:
        match = re.search(r"Thought\s*:\s*(.*?)(?:\nAction\s*:|\nFinal Answer\s*:|$)", text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""

    def _log(self, message: str):
        if self.verbose:
            print(message)

    def get_trace(self) -> list[TraceStep]:
        return self.trace_steps

    def clear_trace(self):
        self.trace_steps = []

    def _format_conversation_history(self) -> str:
        lines = []

        for message in self.history:
            if message.role == "system":
                continue

            if message.role == "user":
                lines.append(f"用户：{message.content}")
            elif message.role == "assistant":
                lines.append(f"助手：{message.content}")

        if not lines:
            return "暂无历史对话。"

        return "\n".join(lines)