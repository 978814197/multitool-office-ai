import lark_oapi as lark

from .config import FeishuConfig


class FeiShuClient:
    """飞书客户端"""

    def __init__(self, config: FeishuConfig):
        """初始化飞书客户端"""
        self.config = config

        self.client = self._build_api_client()

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
