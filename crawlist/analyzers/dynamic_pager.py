from .valid import Valid
from .pager import Pager
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service


class DynamicPager(Pager):
    def __init__(self, webdriver: WebDriver = None) -> None:
        """
        :param webdriver: selenium的WebDriver对象
        """
        if not webdriver:
            option = wd.ChromeOptions()
            option.add_argument("start-maximized")
            option.add_argument("--headless")
            option.add_argument("window-size=1920x3000")
            self.webdriver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        else:
            self.webdriver = webdriver

    def __del__(self):
        try:
            self.webdriver.quit()
        except:
            pass


class DynamicPagerRedirect(DynamicPager):
    def __init__(self, uri: str, uri_split: str, webdriver: WebDriver = None, start: int = 1, offset: int = 1) -> None:
        """
        基于动态网页分析器(重定向)
        :param uri: 第一页链接
        :param uri_split: 链接分页(使用%v代理) example:https://www.boc.cn/sourcedb/whpj/index_%v.html
        :param webdriver: selenium的WebDriver对象
        :param start: 起始页
        :param offset: 分页间隔
        """
        assert '%v' in uri_split
        assert Valid.is_valid_url(uri) and Valid.is_valid_url(uri_split.replace('%v', str(start)))
        assert offset >= 1 and start >= 0
        super().__init__(webdriver=webdriver)
        self.index = start
        self.offset = offset
        self.current_uri = uri
        self.uri_split = uri_split

    def next(self) -> None:
        self.index += self.offset
        self.current_uri = self.uri_split.replace('%v', str(self.index))

    @property
    def html(self) -> str:
        self.webdriver.get(self.current_uri)
        return self.webdriver.page_source


class DynamicPagerListRedirect(DynamicPager):
    def __init__(self, uris: list, webdriver: WebDriver = None) -> None:
        """
        基于动态网页分析器(重定向)
        :param uris: 含多个uri的list，按照顺序往下执行
        :param webdriver: selenium的WebDriver对象
        """
        assert isinstance(uris, list)
        for uri in uris:
            assert Valid.is_valid_url(uri)
        assert len(uris) > 0
        super().__init__(webdriver=webdriver)
        self.index = 0
        self.uris = uris

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
