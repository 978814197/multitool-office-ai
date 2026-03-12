from .bots import FeiShuBot, ChannelEnum
from .config import ClientConfig


class MultitoolOfficeAiClient:
    """多工具办公 AI 客户端"""

    def __init__(self, config: ClientConfig):
        """
        初始化多工具办公 AI 客户端

        :param config: 客户端配置
        """
        self.config = config

    def start(self) -> None:
        """启动渠道"""
        match self.config.channel:
            case ChannelEnum.FEISHU:
                bot = FeiShuBot(self.config.channel_config)
                bot.start()
            case _:
                raise ValueError(f"Unsupported channel: {self.config.channel}")
