import random
import time

from crawlist.annotation import check


class BasePager(object):
    pass


class Pager(BasePager):

    @check
    def __init__(self, interval: float = 0.1):
        """
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
        self.interval: float = interval
        self.half_interval: float = interval / 2

    def next(self) -> None:
        """
        Data Incremental Method
        """
        raise NotImplementedError

    @property
    def html(self) -> str:
        """
        HTML text in the current state
        :return: The html text
        """
        raise NotImplementedError

    def __call__(self):
        self.next()

    def sleep(self):
        time.sleep(random.uniform(self.half_interval / 2, self.interval))


