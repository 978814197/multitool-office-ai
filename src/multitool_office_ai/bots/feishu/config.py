import lark_oapi as lark
from pydantic import BaseModel


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
