from .agents import SupervisorAgent
from .bots import FeiShuBot, ChannelEnum
from .config import ClientConfig
from .core.logging_config import setup_logging

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
        # 配置日志
        setup_logging(
            log_level=self.config.logging_config.level,
            log_file=self.config.logging_config.log_file,
            log_dir=self.config.logging_config.log_dir,
            console_output=self.config.logging_config.console_output
        )

        # 创建主 Agent
        agent = SupervisorAgent(self.config.supervisor_agent_config)
        # 创建渠道
        match self.config.channel:
            case ChannelEnum.FEISHU:
                bot = FeiShuBot(self.config.channel_config, agent)
            case _:
                raise ValueError(f"Unsupported channel: {self.config.channel}")
        # 启动机器人
        bot.start()
