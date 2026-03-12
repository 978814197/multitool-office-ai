import asyncio
import json
import traceback
from logging import getLogger
from queue import Queue

import lark_oapi as lark
from langchain_core.messages import HumanMessage
from lark_oapi.api.im.v1 import P2ImMessageReceiveV1, ReplyMessageRequest, ReplyMessageRequestBody

from .config import FeishuConfig
from ...agents import SupervisorAgent

logger = getLogger("multitool_office_ai")


class FeishuActuator:
    """飞书机器人执行器"""

    def __init__(self, config: FeishuConfig, agent: SupervisorAgent):
        """初始化飞书机器人执行器"""
        self.config = config
        self.agent = agent

        # 定义循环标志位
        self.is_running = True

        # 创建飞书客户端
        self.client = self._build_api_client()

        # 创建任务队列
        self.data_queue = Queue()

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

    async def run_loop(self):
        """
        处理任务队列的主循环方法。

        该方法是一个异步函数，保持运行状态以连续从任务队列中提取任务并执行。

        :raises asyncio.CancelledError: 当事件循环取消该任务时可能引发此异常。
        """
        while self.is_running:
            try:
                # 判断队列是否为空
                if self.data_queue.empty():
                    await asyncio.sleep(1.0)
                    continue
                # 等待任务
                data = await asyncio.get_event_loop().run_in_executor(
                    None, self.data_queue.get, True, 1.0
                )

                # 执行任务
                try:
                    await self.process_task(data)
                finally:
                    self.data_queue.task_done()

            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                logger.info("Actuator task loop cancelled")
                break
            except Exception as e:
                logger.error(f"Actuator task processing error: {e}")
                traceback.print_exc()

    def start(self):
        """
        启动飞书机器人执行器以执行任务。

        此方法用于启动飞书机器人执行器并开始处理任务队列中的任务。
        """
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.run_loop())
        finally:
            loop.close()

    async def process_task(self, data: P2ImMessageReceiveV1):
        """处理单个任务"""
        # 获取消息内容
        content = json.loads(data.event.message.content)
        result = await self.agent.chat(HumanMessage(content=content["text"]))
        logger.info(f"Received message: {content['text']}, response: {result}")
        await self.send_response(data, result)

    async def send_response(self, data: P2ImMessageReceiveV1, result):
        """发送响应到飞书"""
        # 构造消息
        message = (
            ReplyMessageRequest.builder()
            .message_id(data.event.message.message_id)
            .request_body(
                ReplyMessageRequestBody.builder()
                .content(json.dumps({"text": result}, ensure_ascii=False))
                .msg_type("text")
                .build()
            )
            .build()
        )
        # 回复消息
        await self.client.im.v1.message.areply(message)

    async def send_error(self, data: P2ImMessageReceiveV1, error_msg):
        """发送错误消息到飞书"""
        # TODO: 实现错误发送逻辑
        pass
