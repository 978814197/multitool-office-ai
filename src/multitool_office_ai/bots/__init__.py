from enum import IntEnum

from .feishu import FeishuConfig, FeiShuBot


class ChannelEnum(IntEnum):
    """机器人渠道"""
    FEISHU = 1
