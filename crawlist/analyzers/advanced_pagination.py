from .valid import Valid
from .pagination import Pagination
from selenium.webdriver.remote.webdriver import WebDriver


class AdvancedPaginationRedirect(Pagination):
    def __init__(self, webdriver: WebDriver, uri: str, uri_split: str, start: int = 1, offset: int = 1) -> None:
        """
        基于静态网页分析器
        :param webdriver: selenium的WebDriver对象
        :param uri: 第一页链接
        :param uri_split: 链接分页(使用%v代理) example:https://www.boc.cn/sourcedb/whpj/index_%v.html
        :param start: 起始页
        :param offset: 分页间隔
        """
        assert '%v' in uri_split
        assert Valid.is_valid_url(uri) and Valid.is_valid_url(uri_split.replace('%v', str(start)))
        assert offset >= 1 and start >= 0
        self.index = start
        self.offset = offset
        self.current_uri = uri
        self.uri_split = uri_split
        self.webdriver = webdriver

    def next(self) -> None:
        self.index += self.offset
        self.current_uri = self.uri_split.replace('%v', str(self.index))

    @property
    def html(self) -> str:
        self.webdriver.get(self.current_uri)
        return self.webdriver.page_source


class AdvancedPaginationListRedirect(Pagination):
    def __init__(self, webdriver: WebDriver, uris: list) -> None:
        """
        基于静态网页分析器
        :param webdriver: selenium的WebDriver对象
        :param uris: 含多个uri的list，按照顺序往下执行
        """
        assert isinstance(uris, list)
        for uri in uris:
            assert Valid.is_valid_url(uri)
        assert len(uris) > 0
        self.index = 0
        self.uris = uris
        self.webdriver = webdriver

    def next(self) -> None:
        if self.index >= len(self.uris):
            return
        self.index += 1

    @property
    def html(self) -> str:
        if self.index >= len(self.uris):
            return ""
        uri = self.uris[self.index]
        self.webdriver.get(uri)
        return self.webdriver.page_source

