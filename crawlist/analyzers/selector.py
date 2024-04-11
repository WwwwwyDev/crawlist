import parsel
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.common.by import By

from .valid import Valid


class BaseSelector(object):
    pass


class Selector(BaseSelector):
    def __init__(self, pattern: str) -> None:
        """
        选择器
        :param pattern: 抓取规则
        """
        assert self.valid(pattern)
        self.pattern = pattern

    def select(self, html: str) -> list[str]:
        raise NotImplementedError

    def valid(self, pattern) -> bool:
        raise NotImplementedError

    def __call__(self, html: str) -> list[str]:
        return self.select(html)


class WebElementSelector(BaseSelector):
    def __init__(self, pattern: str) -> None:
        """
        webElement选择器(selenium)
        :param pattern: 抓取规则
        """
        assert self.valid(pattern)
        self.pattern = pattern

    def select(self, webdriver: WebDriver, interval: float = 0.1) -> list[WebElement]:
        raise NotImplementedError

    def valid(self, pattern) -> bool:
        raise NotImplementedError

    def __call__(self, webdriver: WebDriver, interval: float = 0.1) -> list[WebElement]:
        return self.select(webdriver, interval)


class CssSelector(Selector):
    """
    css选择器
    """

    def select(self, html: str) -> list[str]:
        return parsel.Selector(text=html).css(self.pattern).getall()

    def valid(self, pattern) -> bool:
        return Valid.is_valid_css(pattern)


class XpathSelector(Selector):
    """
    xpath选择器
    """

    def select(self, html: str) -> list[str]:
        return parsel.Selector(text=html).xpath(self.pattern).getall()

    def valid(self, pattern) -> bool:
        return Valid.is_valid_xpath(pattern)


class RegexSelector(Selector):
    """
    正则表达式选择器
    """

    def select(self, html: str) -> list[str]:
        return parsel.Selector(text=html).re(self.pattern)

    def valid(self, pattern) -> bool:
        return Valid.is_valid_regex(pattern)


class CssWebElementSelector(WebElementSelector):

    def select(self, webdriver: WebDriver, interval: float = 0.1) -> list[WebElement]:
        WebDriverWait(webdriver, interval).until(
            Ec.presence_of_element_located((By.CSS_SELECTOR, self.pattern)))
        return webdriver.find_elements(
            By.CSS_SELECTOR, self.pattern)

    def valid(self, pattern) -> bool:
        return Valid.is_valid_css(pattern)


class XpathWebElementSelector(WebElementSelector):

    def select(self, webdriver: WebDriver, interval: float = 0.1) -> list[WebElement]:
        WebDriverWait(webdriver, interval).until(
            Ec.presence_of_element_located((By.XPATH, self.pattern)))
        return webdriver.find_elements(
            By.XPATH, self.pattern)

    def valid(self, pattern) -> bool:
        return Valid.is_valid_xpath(pattern)


