from abc import ABCMeta, abstractmethod


class BaseBot(metaclass=ABCMeta):
    """
    一个描述 BaseBot 的基类。

    BaseBot 是一个抽象基类，该类定义了机器人需要实现的接口和行为的基础框架。
    此类不能直接实例化，而是需要通过继承来扩展其功能。
    """

    @abstractmethod
    def start(self):
        """
        启动事件客户端。

        该方法用于启动事件客户端，使其开始工作。

        :return: 无返回值。
        """
        raise NotImplementedError
