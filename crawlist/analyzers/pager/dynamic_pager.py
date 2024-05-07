import parsel
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

from crawlist.analyzers.pager.pager import Pager
from crawlist.analyzers.driver import Driver, DefaultDriver
from crawlist.analyzers.valid import Valid
from crawlist.analyzers.selector import WebElementSelector
from crawlist.annotation import check


class DynamicPager(Pager):
    @check
    def __init__(self, webdriver: Driver | WebDriver = None, interval: float = 0.1) -> None:
        """
        :param webdriver: WebDriver object for selenium
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
        self.default_driver_flag = False
        if not webdriver:
            self.default_driver_flag = True
            self.webdriver = DefaultDriver()()
        else:
            if isinstance(webdriver, WebDriver):
                self.webdriver = webdriver
            else:
                self.webdriver = webdriver()
        super().__init__(interval=interval)

    def click_safety(self, button: WebElement) -> None:
        """
        Attempt to click the button multiple times
        :param button: Button elements
        """
        # Multiple attempts to click after failed clicks
        for _ in range(3):
            try:
                button.click()
                self.sleep()
                break
            except Exception:
                pass

    def pre_load(self, webdriver: WebDriver) -> None:
        pass

    def __del__(self):
        if self.default_driver_flag:
            try:
                self.webdriver.quit()
            except:
                pass


class DynamicRedirectPager(DynamicPager):
    @check
    def __init__(self, uri: str, uri_split: str, webdriver: Driver | WebDriver = None, start: int = 1, offset: int = 1,
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
        self.index = start
        self.offset = offset
        self.current_uri = uri
        self.uri_split = uri_split
        super().__init__(webdriver=webdriver, interval=interval)
        self.pre_load(self.webdriver)
        self.sleep()

    def next(self) -> None:
        self.index += self.offset
        self.current_uri = self.uri_split.replace('%v', str(self.index))
        self.sleep()

    @property
    def html(self) -> str:
        self.webdriver.get(self.current_uri)
        return self.webdriver.page_source


class DynamicListRedirectPager(DynamicPager):
    @check
    def __init__(self, uris: list, webdriver: Driver | WebDriver = None, interval: float = 0.1) -> None:
        """
        Based on dynamic web page analyzer (redirect page flipping)
        :param uris: A list containing multiple uris, executed in order downwards
        :param webdriver: WebDriver object for selenium
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
        for uri in uris:
            assert Valid.is_valid_url(uri)
        assert len(uris) > 0
        self.uris = uris
        self.index = 0
        super().__init__(webdriver=webdriver, interval=interval)
        self.pre_load(self.webdriver)
        self.sleep()

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
    @check
    def __init__(self, uri: str, webdriver: Driver | WebDriver = None, interval: float = 1) -> None:
        """
        Based on dynamic web page analyzer (scrolling and flipping)
        :param uri: webpage link, which is a scrolling page
        :param webdriver: WebDriver object for selenium
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
        assert Valid.is_valid_url(uri)
        self.uri = uri
        super().__init__(webdriver=webdriver, interval=interval)
        self.pre_load(self.webdriver)
        self.sleep()

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
        actions = ActionChains(self.webdriver)
        actions.move_by_offset(0, 0).click().perform()
        self.sleep()
        for _ in range(5):
            actions.send_keys(Keys.SPACE).perform()
            self.sleep()
        self.sleep()

    @property
    def html(self) -> str:
        return self.webdriver.page_source

    def pre_load(self, webdriver: WebDriver) -> None:
        webdriver.get(self.uri)


class DynamicLineButtonPager(DynamicPager):
    @check
    def __init__(self, uri: str, button_selector: WebElementSelector, webdriver: Driver | WebDriver = None,
                 interval: float = 1) -> None:
        """
        Based on dynamic web page analyzer (row button page flipping)
        :param uri: webpage link, which is a row button for flipping pages
        :param button.selector: row button selector
        :param webdriver: WebDriver object for selenium
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
        assert Valid.is_valid_url(uri)
        self.uri = uri
        super().__init__(webdriver=webdriver, interval=interval)
        self.pre_load(self.webdriver)
        self.sleep()
        assert len(button_selector(self.webdriver, interval=interval)) > 0
        self.button = button_selector

    def next(self) -> None:
        button_element = self.button(self.webdriver, interval=self.interval)[0]
        self.click_safety(button_element)
        self.sleep()

    @property
    def html(self) -> str:
        return self.webdriver.page_source

    def pre_load(self, webdriver: WebDriver) -> None:
        webdriver.get(self.uri)


class DynamicNumButtonPager(DynamicPager):
    @check
    def __init__(self, uri: str, button_selector: WebElementSelector, webdriver: Driver | WebDriver = None, start: int = 1,
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
        self.uri = uri
        super().__init__(webdriver=webdriver, interval=interval)
        self.pre_load(self.webdriver)
        self.sleep()
        assert len(button_selector(self.webdriver, interval=interval)) > 0
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
        Find if there are numbers in the inner_text of an element
        :param element: selenium WebElement
        :param num: Specific numbers for judgment
        :return: Is there a number
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
        Searching for elements that meet the criteria within a set of elements
        :param elements: selenium WebElement lists
        :param num: Required Numbers
        :return: The selected button, if not found, is None
        """
        for element in elements:
            if DynamicNumButtonPager.check_num_button(element, num):
                return element
        return None

    def pre_load(self, webdriver: WebDriver) -> None:
        webdriver.get(self.uri)


class DynamicNextButtonPager(DynamicPager):
    @check
    def __init__(self, uri: str, button_selector: WebElementSelector, webdriver: Driver | WebDriver = None, start: int = 1,
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
        self.uri = uri
        super().__init__(webdriver=webdriver, interval=interval)
        self.pre_load(self.webdriver)
        self.sleep()
        assert len(button_selector(self.webdriver, interval=interval)) > 0
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

    def pre_load(self, webdriver: WebDriver) -> None:
        webdriver.get(self.uri)
