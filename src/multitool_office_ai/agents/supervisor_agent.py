from typing import Annotated, Any

from langchain_core.messages import AnyMessage, HumanMessage
from langchain_openai.chat_models import ChatOpenAI
from langgraph.constants import START, END
from langgraph.graph import add_messages
from langgraph.graph.state import CompiledStateGraph, StateGraph
from pydantic import BaseModel, SecretStr


class SupervisorAgentConfig(BaseModel):
    """主 Agent 的配置"""
    # api端点
    base_url: str
    # api 密钥
    api_key: SecretStr
    # 模型
    model: str


class SupervisorAgentState(BaseModel):
    """主 Agent 的状态"""
    # 上下文列表
    messages: Annotated[list[AnyMessage], add_messages]


class SupervisorAgent:
    """主 Agent"""

    def __init__(self, config: SupervisorAgentConfig):
        """初始化主 Agent"""
        self.config = config

        self.llm = self._build_llm()

        self.graph = self._build_graph()

    def _build_llm(self) -> ChatOpenAI:
        """
        构建并返回一个 ChatOpenAI 实例。

        本方法用于根据当前配置初始化并返回一个 ChatOpenAI 实例。该实例将具备所有必要的参数，允许基于配置完成
        自然语言处理相关任务。

        :return: 返回已初始化的 ChatOpenAI 实例
        :rtype: ChatOpenAI
        """
        return ChatOpenAI(
            base_url=self.config.base_url,
            api_key=self.config.api_key,
            model=self.config.model
        )

    def _build_graph(self) -> CompiledStateGraph:
        """
        构建状态图并配置其节点与边。

        :raises Exception: 如果状态图的配置过程中发生错误。
        :return: 已编译的状态图实例。
        :rtype: CompiledStateGraph
        """
        workflow = StateGraph(SupervisorAgentState)

        # 添加 LLM 节点
        workflow.add_node("llm", self._call_llm)

        # 定义边：START -> llm -> END
        workflow.add_edge(START, "llm")
        workflow.add_edge("llm", END)

        return workflow.compile()

    async def _call_llm(self, state: SupervisorAgentState) -> dict[str, Any]:
        """
        调用 LLM 并返回更新后的状态。

        :param state: SupervisorAgentState 类型，对象包含需要传递给 LLM 的消息。
        :return: 一个字典，包含更新后的消息列表，键为 "messages"。
        """
        # 调用 LLM
        response = await self.llm.ainvoke(state.messages)

        # 返回更新的状态
        return {"messages": [response]}

    async def chat(self, message: HumanMessage) -> str:
        """
        与 LLM 进行对话，处理用户消息并返回响应。

        :param message: HumanMessage 类型，用户输入的消息。
        :return: LLM 的响应文本。
        """
        # 创建初始状态
        initial_state = SupervisorAgentState(
            messages=[message]
        )

        # 运行图
        result = await self.graph.ainvoke(initial_state)

        # 获取结果
        return result["messages"][-1].content if result["messages"] else ""
