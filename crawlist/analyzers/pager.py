class BasePager(object):
    pass


class Pager(BasePager):

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
