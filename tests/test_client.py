import os

from langchain_core.messages import HumanMessage

from multitool_office_ai import MultitoolOfficeAiClient, ClientConfig


async def test_client():
    """
    这是一个异步函数，用于创建并返回一个 MultitoolOfficeAiClient 实例。

    :returns: 创建的 MultitoolOfficeAiClient 实例
    :rtype: MultitoolOfficeAiClient
    """
    # 创建客户端配置
    config = ClientConfig(
        base_url=os.environ["MULTITOOFICE_BASE_URL"],
        api=os.environ["MULTITOOFICE_API"],
        api_key=os.environ["MULTITOOFICE_API_KEY"],
        model=os.environ["MULTITOOFICE_MODEL"],
    )
    # 创建客户端
    client = MultitoolOfficeAiClient(config=config)
    # 开始执行
    while True:
        await client.chat(HumanMessage(content="你好"))
