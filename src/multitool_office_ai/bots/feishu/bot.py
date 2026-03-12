import lark_oapi as lark

from .config import FeishuConfig
from ..base import BaseBot
from ...agents import SupervisorAgent


class FeiShuBot(BaseBot):
    """
    飞书机器人类的摘要。

    此类用于表示一个飞书机器人，继承自 BaseBot，主要用于处理飞书相关的交互和功能扩展。
    """

    def __init__(self, config: FeishuConfig, agent: SupervisorAgent):
        """初始化飞书机器人"""
        self.config = config

        self.event_client = self._build_event_client()

    def _build_event_client(self) -> lark.ws.Client:
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
