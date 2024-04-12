from .request import Request
from .valid import Valid
from .pager import Pager


class StaticPager(Pager):
    def __init__(self, request: Request = None, interval: float = 0.1):
        """
        :param request: 请求对象
        :param interval: 抓取list频率，可使用self.sleep()方法控制频率
        """
        if not request:
            self.request = Request(headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
                'Cache-Control': 'max-age=0',
            })
        else:
            self.request = request
        super().__init__(interval=interval)


class StaticRedirectPager(StaticPager):
    def __init__(self, uri: str, uri_split: str, request: Request = None, start: int = 1, offset: int = 1,
                 interval: float = 0.1) -> None:
        """
        基于静态网页分析器(重定向翻页)
        :param uri: 第一页链接
        :param uri_split: 链接分页(使用%v代替) example:https://www.boc.cn/sourcedb/whpj/index_%v.html
        :param request: 请求对象
        :param start: 起始页
        :param offset: 分页间隔
        :param interval: 抓取list频率，可使用self.sleep()方法控制频率
        """
        assert '%v' in uri_split
        assert Valid.is_valid_url(uri) and Valid.is_valid_url(uri_split.replace('%v', str(start)))
        assert offset >= 1 and start >= 0
        super().__init__(request=request, interval=interval)
        self.index = start
        self.offset = offset
        self.current_uri = uri
        self.uri_split = uri_split

    def next(self) -> None:
        self.index += self.offset
        self.current_uri = self.uri_split.replace('%v', str(self.index))
        self.sleep()

    @property
    def html(self) -> str:
        return self.request(self.current_uri)


class StaticListRedirectPager(StaticPager):
    def __init__(self, uris: list, request: Request = None, interval: float = 0.1) -> None:
        """
        基于静态网页分析器(重定向翻页)
        :param uris: 含多个uri的list，按照顺序往下执行
        :param request: 请求对象
        :param interval: 抓取list频率，可使用self.sleep()方法控制频率
        """
        assert isinstance(uris, list)
        for uri in uris:
            assert Valid.is_valid_url(uri)
        assert len(uris) > 0
        super().__init__(request=request, interval=interval)
        self.index = 0
        self.uris = uris

    def next(self) -> None:
        if self.index >= len(self.uris):
            return
        self.index += 1
        self.sleep()

    @property
    def html(self) -> str:
        if self.index >= len(self.uris):
            return ""
        uri = self.uris[self.index]
        return self.request(uri)
