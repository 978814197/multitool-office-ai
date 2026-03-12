import lark_oapi as lark
from pydantic import BaseModel

from .base import BaseBot


class FeishuConfig(BaseModel):
    """飞书机器人配置"""
    # 应用的 App ID
    app_id: str
    # App 密钥
    app_secret: str
    # 飞书域名
    domain: str = lark.FEISHU_DOMAIN
    # 超时时间（秒）
    timeout: int = 3
    # 应用类型
    app_type: lark.AppType = lark.AppType.SELF
    # 应用的 app_access_token
    app_ticket: str = ""
    # 是否允许手动设置token
    enable_set_token: bool = False
    # 日志级别
    log_level: lark.LogLevel = lark.LogLevel.DEBUG


class FeiShuBot(BaseBot):
    """
    飞书机器人类的摘要。

    此类用于表示一个飞书机器人，继承自 BaseBot，主要用于处理飞书相关的交互和功能扩展。
    """

    def __init__(self, config: FeishuConfig):
        """
        为该类的实例初始化一个 Feishu API 客户端和一个 WebSocket 客户端。

        :param config: FeishuConfig 配置对象，用于提供初始化客户端所需的应用 ID、应用密钥、域名、
            超时时间、应用类型、应用票据、令牌设置和日志级别等参数。
        :type config: FeishuConfig
        """
        self.config = config

        self.api_client = self._build_api_client

        self.event_client = self._build_event_client()

    def _build_api_client(self) -> lark.Client:
        """
        构建并返回一个配置好的 lark.Client 对象。

        该方法用于根据当前实例的配置，创建并初始化一个 `lark.Client` 对象。
        通过从 `self.config` 配置对象中读取相关参数，可以确保生成的 `lark.Client`
        满足所需的特定需求，同时支持定制化配置，例如超时、日志级别等。

        :return: 配置好的 lark.Client 对象
        :rtype: lark.Client
        """
        return (
            lark.Client.builder()
            .app_id(self.config.app_id)
            .app_secret(self.config.app_secret)
            .domain(self.config.domain)
            .timeout(self.config.timeout)
            .app_type(self.config.app_type)
            .app_ticket(self.config.app_ticket)
            .enable_set_token(self.config.enable_set_token)
            .log_level(self.config.log_level)
            .build()
        )

    def _build_event_client(self):
        """
        创建事件客户端，并配置消息接收和自定义事件处理程序。

        :returns: 配置完成的事件客户端实例
        :rtype: lark.ws.Client
        """
        event_handler = (
            lark.EventDispatcherHandler.builder("", "")
            .register_p2_im_message_receive_v1(self.do_p2_im_message_receive_v1)
            .build()
        )
        return lark.ws.Client(
            self.config.app_id,
            self.config.app_secret,
            event_handler=event_handler,
            log_level=self.config.log_level,
        )

    def do_p2_im_message_receive_v1(self, data: lark.im.v1.P2ImMessageReceiveV1) -> None:
        """
        处理 P2ImMessageReceiveV1 类型的消息。

        该方法用于处理飞书平台的 P2ImMessageReceiveV1 类型的消息，包括打印消息内容等操作。

        :param data: P2ImMessageReceiveV1 类型的消息数据
        :type data: lark.im.v1.P2ImMessageReceiveV1
        :return: 无返回值。
        """
        print(data.event.message.content)
        print(data.event.message.message_type)

    def start(self):
        """
        启动事件客户端。

        该方法用于启动事件客户端，使其开始工作。

        :return: 无返回值。
        """
        self.event_client.start()
