import random
import time


class BasePager(object):
    pass


class Pager(BasePager):

    def __init__(self, interval: float = 0.1):
        """
        :param interval: 抓取list频率，可使用self.sleep()方法控制频率
        """
        self.interval: float = interval
        self.half_interval: float = interval / 2

    def next(self) -> None:
        """
        数据增量方法
        :return:
        """
        raise NotImplementedError

    @property
    def html(self) -> str:
        """
        当前状态的html文本
        :return:
        """
        raise NotImplementedError

    def __call__(self):
        self.next()

    def sleep(self):
        time.sleep(random.uniform(self.half_interval / 2, self.interval))


