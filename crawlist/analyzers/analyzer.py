# 分析器父类对象，需要子类实现
from typing import Any, Generator


class BaseAnalyzer:
    """
    分析器接口,需要子类方法实现
    """

    def list(self, limit: int) -> Generator[Any, Any, None]:
        """
        列表生成器接口，每次生成一条数据
        :param limit: 取最新的条数
        :return: 抓取到的格式化list
        """
        for element in self.crawl(limit=limit):
            yield self.after(element)

    def crawl(self, limit: int) -> Generator[Any, str, None]:
        raise NotImplementedError

    def after(self, html: str) -> Any:
        raise NotImplementedError


class Analyzer(BaseAnalyzer):
    """
    分析器父类,需要子类方法实现
    """

    def __init__(self, uri: str, selector: str, rule: str = "xpath", interval: float = 0.1) -> None:
        """
        分析器接口,需要子类方法实现
        :param uri: 需要爬取列表的uri
        :param selector: 抽取list的选择题
        :param rule: 抽取规则(xpath, css, re)
        :param interval: 分析器执行间隔
        """
        assert rule in {"xpath", "css", "re"}
        self.analyzer_url = uri
        self.rule = rule
        self.selector = selector
        self.interval = interval
        self.is_max = False  # 是否已到最后一页

    def list(self, limit: int) -> Generator[Any, Any, None]:
        """
        列表生成器接口，每次生成一条数据
        :param limit: 取最新的条数
        :return: 抓取到的格式化list
        """
        for element in self.crawl(limit=limit):
            yield self.after(element)

    def crawl(self, limit: int) -> Generator[Any, str, None]:
        raise NotImplementedError

    def after(self, html: str) -> Any:
        return html
