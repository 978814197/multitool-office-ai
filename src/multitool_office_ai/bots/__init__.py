from enum import IntEnum

from .feishu import FeishuConfig, FeiShuBot, FeiShuClient


class ChannelEnum(IntEnum):
    """机器人渠道"""
    FEISHU = 1
