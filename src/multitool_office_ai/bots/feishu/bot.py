from concurrent.futures import ThreadPoolExecutor

import lark_oapi as lark

from .actuator import FeishuActuator
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

        self.actuator = FeishuActuator(self.config, agent)

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
        self.actuator.task_queue.put_nowait(data)

    def start(self):
        """
        启动事件客户端。

        该方法用于启动事件客户端，使其开始工作。

        :return: 无返回值。
        """
        # 创建线程池
        pool = ThreadPoolExecutor(max_workers=2, thread_name_prefix="FeishuBot")

        try:
            # 提交任务
            pool.submit(self._run_actuator)
            pool.submit(self._run_event_client)

            # 阻塞主线程，等待所有任务完成
            pool.shutdown(wait=True)

        except KeyboardInterrupt:
            print("\n[FeiShuBot] 收到停止信号")
        finally:
            # 清理资源
            pool.shutdown(wait=True, cancel_futures=True)
            print("[FeiShuBot] 服务已停止")

    def _run_actuator(self):
        """
        调用执行器以启动其操作。

        :raises RuntimeError: 如果执行器未正确初始化或无法启动。
        """
        self.actuator.start()

    def _run_event_client(self):
        """
        启动事件客户端以处理事件流。

        此方法用于启动事件客户端并确保事件流的正常操作。

        :return: 无返回值
        """
        self.event_client.start()
