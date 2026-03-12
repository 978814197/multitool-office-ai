import os

from multitool_office_ai.bots import FeishuConfig, FeiShuBot


def test_feishu_bot():
    """测试飞书机器人"""
    config = FeishuConfig(
        app_id=os.environ['FEISHU_BOT_APP_ID'],
        app_secret=os.environ['FEISHU_BOT_APP_SECRET'],
    )
    bot = FeiShuBot(config)
    bot.start()
