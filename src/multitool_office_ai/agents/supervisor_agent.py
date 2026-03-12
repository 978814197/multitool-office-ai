from typing import Annotated

from langchain_core.messages import AnyMessage
from langgraph.graph import add_messages
from langgraph.graph.state import CompiledStateGraph, StateGraph
from pydantic import BaseModel


class SupervisorAgentConfig(BaseModel):
    """主 Agent 的配置"""
    # api端点
    base_url: str
    # api
    api: str
    # api 密钥
    api_key: str
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
        self.graph = self._build_graph()

    def _build_graph(self) -> CompiledStateGraph:
        """
        构建状态图并配置其节点与边。

        :raises Exception: 如果状态图的配置过程中发生错误。
        :return: 已编译的状态图实例。
        :rtype: CompiledStateGraph
        """
        workflow = StateGraph(SupervisorAgentState)
        return workflow.compile()
