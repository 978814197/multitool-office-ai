from pydantic import BaseModel

from .agents import SupervisorAgentConfig
from .bots import ChannelEnum, FeishuConfig


class ClientConfig(BaseModel):
    """客户端配置"""
    # 主 Agent 配置
    supervisor_agent_config: SupervisorAgentConfig

    # 使用的机器人渠道
    channel: ChannelEnum
    # 渠道配置
    channel_config: FeishuConfig
