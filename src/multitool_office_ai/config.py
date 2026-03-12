from typing import Literal

from pydantic import BaseModel

from .agents import SupervisorAgentConfig
from .bots import ChannelEnum, FeishuConfig


class LoggingConfig(BaseModel):
    """日志配置"""
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    log_file: str = "app.log"
    log_dir: str = "logs"
    console_output: bool = True


class ClientConfig(BaseModel):
    """客户端配置"""
    # 日志配置
    logging_config: LoggingConfig = LoggingConfig()

    # 主 Agent 配置
    supervisor_agent_config: SupervisorAgentConfig

    # 使用的机器人渠道
    channel: ChannelEnum
    # 渠道配置
    channel_config: FeishuConfig
