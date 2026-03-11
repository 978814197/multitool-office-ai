from pydantic import BaseModel


class ClientConfig(BaseModel):
    """客户端配置"""
    # api端点
    base_url: str
    # api
    api: str
    # api 密钥
    api_key: str
    # 模型
    model: str
