from langchain_core.messages import HumanMessage, AIMessage

from .config import ClientConfig


class MultitoolOfficeAiClient:
    """多工具办公 AI 客户端"""

    def __init__(self, config: ClientConfig):
        """
        初始化多工具办公 AI 客户端

        :param config: 客户端配置
        """
        self.config = config

    async def chat(self, message: HumanMessage) -> AIMessage:
        """执行多工具办公 AI 客户端"""
        pass
