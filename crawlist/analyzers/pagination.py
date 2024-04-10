class Pagination(object):

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
