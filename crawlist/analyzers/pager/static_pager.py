from crawlist.analyzers.pager.pager import Pager
from crawlist.analyzers.request import Request, DefaultRequest
from crawlist.analyzers.valid import Valid
from crawlist.annotation import check


class StaticPager(Pager):
    @check
    def __init__(self, request: Request = None, interval: float = 0.1):
        """
        :param request: Request object
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
        if not request:
            self.request = DefaultRequest()
        else:
            self.request = request
        super().__init__(interval=interval)


class StaticRedirectPager(StaticPager):
    @check
    def __init__(self, uri: str, uri_split: str, request: Request = None, start: int = 1, offset: int = 1,
                 interval: float = 0.1) -> None:
        """
        Based on static web page analyzer (redirect page flipping)
        :param uri: First page link
        :param uri_split: Link pagination (using %v instead) Example: https://www.boc.cn/sourcedb/whpj/index_%v.html
        :param request: Request object
        :param start: Start page
        :param offset: pagination interval
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
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
    @check
    def __init__(self, uris: list, request: Request = None, interval: float = 0.1) -> None:
        """
        Based on static web page analyzer (redirect page flipping)
        :param uris: A list containing multiple uris, executed in order downwards
        :param request: Request object
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
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
