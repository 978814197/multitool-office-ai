import os

from multitool_office_ai import ClientConfig, MultitoolOfficeAiClient
from multitool_office_ai.agents import SupervisorAgentConfig
from multitool_office_ai.bots import FeishuConfig, ChannelEnum


def test_feishu_bot():
    """测试飞书机器人"""
    # 创建主agent配置
    supervisor_agent_config = SupervisorAgentConfig(
        base_url=os.environ["MULTITOOFICE_BASE_URL"],
        api=os.environ["MULTITOOFICE_API"],
        api_key=os.environ["MULTITOOFICE_API_KEY"],
        model=os.environ["MULTITOOFICE_MODEL"],
    )
    # 创建飞书配置
    channel_config = FeishuConfig(
        app_id=os.environ['FEISHU_BOT_APP_ID'],
        app_secret=os.environ['FEISHU_BOT_APP_SECRET'],
    )
    # 创建客户端配置
    config = ClientConfig(
        supervisor_agent_config=supervisor_agent_config,
        channel=ChannelEnum.FEISHU,
        channel_config=channel_config,
    )
    # 创建客户端
    client = MultitoolOfficeAiClient(config=config)
    # 启动客户端
    client.start()
