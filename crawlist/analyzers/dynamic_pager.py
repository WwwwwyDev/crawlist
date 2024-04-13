import parsel
from selenium.webdriver.remote.webelement import WebElement
from .valid import Valid
from .pager import Pager
from .selector import WebElementSelector
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service


class DynamicPager(Pager):
    def __init__(self, webdriver: WebDriver = None, interval: float = 0.1) -> None:
        """
        :param webdriver: WebDriver object for selenium
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
        if not webdriver:
            option = wd.ChromeOptions()
            option.add_argument("start-maximized")
            option.add_argument("--headless")
            option.add_argument("window-size=1920x3000")
            agent = 'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"'
            option.add_argument(agent)

            self.webdriver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=option)
        else:
            self.webdriver = webdriver
        super().__init__(interval=interval)

    def click_safety(self, button: WebElement) -> None:
        """
        Attempt to click the button multiple times
        :param button: Button elements
        """
        # 点击失败后多次尝试点击
        for _ in range(3):
            try:
                button.click()
                self.sleep()
                break
            except Exception:
                pass

    def pre_load(self, webdriver: WebDriver = None) -> bool:
        return False

    def __del__(self):
        try:
            self.webdriver.quit()
        except:
            pass


class DynamicRedirectPager(DynamicPager):
    def __init__(self, uri: str, uri_split: str, webdriver: WebDriver = None, start: int = 1, offset: int = 1,
                 interval: float = 0.1) -> None:
        """
        Based on dynamic web page analyzer (redirect page flipping)
        :param uri: First page link
        :param uri_split: Link pagination (using% v proxy) Example: https://www.boc.cn/sourcedb/whpj/index_%v.html
        :param webdriver: WebDriver object for selenium
        :param start: Start page
        :param offset: pagination interval
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
        assert '%v' in uri_split
        assert Valid.is_valid_url(uri) and Valid.is_valid_url(uri_split.replace('%v', str(start)))
        assert offset >= 1 and start >= 0
        super().__init__(webdriver=webdriver, interval=interval)
        self.pre_load(webdriver)
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
        self.webdriver.get(self.current_uri)
        return self.webdriver.page_source


class DynamicListRedirectPager(DynamicPager):
    def __init__(self, uris: list, webdriver: WebDriver = None, interval: float = 0.1) -> None:
        """
        Based on dynamic web page analyzer (redirect page flipping)
        :param uris: A list containing multiple uris, executed in order downwards
        :param webdriver: WebDriver object for selenium
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
        assert isinstance(uris, list)
        for uri in uris:
            assert Valid.is_valid_url(uri)
        assert len(uris) > 0
        super().__init__(webdriver=webdriver, interval=interval)
        self.pre_load(webdriver)
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
        self.webdriver.get(uri)
        return self.webdriver.page_source


class DynamicScrollPager(DynamicPager):
    def __init__(self, uri: str, webdriver: WebDriver = None, interval: float = 1) -> None:
        """
        Based on dynamic web page analyzer (scrolling and flipping)
        :param uri: webpage link, which is a scrolling page
        :param webdriver: WebDriver object for selenium
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
        assert Valid.is_valid_url(uri)
        super().__init__(webdriver=webdriver, interval=interval)
        if not self.pre_load(self.webdriver):
            self.webdriver.get(uri)
        self.uri = uri

    js_code = '''he = setInterval(() => {
                        document.documentElement.scrollTop += document.documentElement.scrollHeight
                        if (document.documentElement.scrollTop >= (document.documentElement.scrollHeight - document.documentElement.scrollWidth)) {
                            clearInterval(he)
                        }
                    },100)
                '''

    def next(self) -> None:
        self.webdriver.execute_script(DynamicScrollPager.js_code)
        self.sleep()

    @property
    def html(self) -> str:
        return self.webdriver.page_source


class DynamicLineButtonPager(DynamicPager):
    def __init__(self, uri: str, button_selector: WebElementSelector, webdriver: WebDriver = None,
                 interval: float = 1) -> None:
        """
        Based on dynamic web page analyzer (row button page flipping)
        :param uri: webpage link, which is a row button for flipping pages
        :param button.selector: row button selector
        :param webdriver: WebDriver object for selenium
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
        assert Valid.is_valid_url(uri)
        super().__init__(webdriver=webdriver, interval=interval)
        if not self.pre_load(self.webdriver):
            self.webdriver.get(uri)
        assert len(button_selector(self.webdriver, interval=interval)) > 0
        self.uri = uri
        self.button = button_selector

    def next(self) -> None:
        button_element = self.button(self.webdriver, interval=self.interval)[0]
        self.click_safety(button_element)
        self.sleep()

    @property
    def html(self) -> str:
        return self.webdriver.page_source


class DynamicNumButtonPager(DynamicPager):
    def __init__(self, uri: str, button_selector: WebElementSelector, webdriver: WebDriver = None, start: int = 1,
                 offset: int = 1, interval: float = 1) -> None:
        """
        Based on dynamic web page analyzer (digital button flipping)
        :param uri: webpage link, which is a numeric button for flipping pages
        :param button.selector: numeric button selector
        :param webdriver: WebDriver object for selenium
        :param start: Start page
        :param offset: pagination interval
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
        assert Valid.is_valid_url(uri)
        super().__init__(webdriver=webdriver, interval=interval)
        if not self.pre_load(self.webdriver):
            self.webdriver.get(uri)
        assert len(button_selector(self.webdriver, interval=interval)) > 0
        self.uri = uri
        self.index = 1
        self.offset = offset
        self.button = button_selector
        while start - 1:
            start -= 1
            self.next_one()

    def next(self) -> None:
        offset = self.offset
        while offset:
            self.next_one()
            offset -= 1
        self.sleep()

    def next_one(self) -> None:
        self.index += 1
        num_button_elements = self.button(self.webdriver, interval=self.interval)
        button = DynamicNumButtonPager.find_num_button(num_button_elements, num=self.index)
        if button:
            self.click_safety(button)
        self.sleep()

    @property
    def html(self) -> str:
        return self.webdriver.page_source

    @staticmethod
    def check_num_button(element: WebElement, num: int = 1) -> bool:
        """
        查找元素的inner_text中是否有数字
        :param element: selenium WebElement
        :param num: 判断的具体数字
        :return: 是否有数字
        """
        html = element.text
        inner_text = html
        try:
            selector = parsel.Selector(html)
            inner_text = "".join(selector.xpath(".//text()").getall())
        except:
            pass
        return str(num) in inner_text

    @staticmethod
    def find_num_button(elements: list[WebElement], num: int = 1) -> WebElement | None:
        """
        在一组元素中，寻找符合条件的元素
        :param elements: selenium WebElement列表
        :param num: 需要的数字
        :return: 选中的按钮，没找到则为None
        """
        for element in elements:
            if DynamicNumButtonPager.check_num_button(element, num):
                return element
        return None


class DynamicNextButtonPager(DynamicPager):
    def __init__(self, uri: str, button_selector: WebElementSelector, webdriver: WebDriver = None, start: int = 1,
                 offset: int = 1, interval: float = 1) -> None:
        """
        Based on dynamic web page analyzer (click the next page button to page)
        :param uri: Web page link, which is a page that can be flipped by clicking the next page button
        :param button.selector: Click on the next page button selector
        :param webdriver: WebDriver object for selenium
        :param start: Start page
        :param offset: pagination interval
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
        assert Valid.is_valid_url(uri)
        super().__init__(webdriver=webdriver, interval=interval)
        if not self.pre_load(self.webdriver):
            self.webdriver.get(uri)
        assert len(button_selector(self.webdriver, interval=interval)) > 0
        self.uri = uri
        self.offset = offset
        self.button = button_selector
        while start - 1:
            start -= 1
            self.next_one()

    def next(self) -> None:
        offset = self.offset
        while offset:
            self.next_one()
            offset -= 1
        self.sleep()

    def next_one(self) -> None:
        button = self.button(self.webdriver, interval=self.interval)[0]
        if button:
            self.click_safety(button)
        self.sleep()

    @property
    def html(self) -> str:
        return self.webdriver.page_source
