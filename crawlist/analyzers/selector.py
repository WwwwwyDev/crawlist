import parsel
from .valid import Valid


class BaseSelector(object):
    pass


class Selector(BaseSelector):
    def __init__(self, pattern: str) -> None:
        assert self.valid(pattern)
        self.pattern = pattern

    def select(self, html: str) -> list[str]:
        raise NotImplementedError

    def valid(self, pattern) -> bool:
        raise NotImplementedError

    def __call__(self, html: str) -> list[str]:
        return self.select(html)


class CssSelector(Selector):

    def select(self, html: str) -> list[str]:
        return parsel.Selector(text=html).css(self.pattern).getall()

    def valid(self, pattern) -> bool:
        return Valid.is_valid_css(pattern)


class XpathSelector(Selector):

    def select(self, html: str) -> list[str]:
        return parsel.Selector(text=html).xpath(self.pattern).getall()

    def valid(self, pattern) -> bool:
        return Valid.is_valid_xpath(pattern)


class RegexSelector(Selector):

    def select(self, html: str) -> list[str]:
        return parsel.Selector(text=html).re(self.pattern)

    def valid(self, pattern) -> bool:
        return Valid.is_valid_regex(pattern)