import random
import time
from typing import Any, Generator
from .selector import Selector
from .pager import Pager


class BaseAnalyzer(object):
    """
    分析器接口,需要子类方法实现
    """

    def __init__(self, interval: float = 0.1) -> None:
        """
        :param interval: 抓取list频率
        """
        self.interval: float = interval
        self.half_interval: float = interval / 2

    def list(self, limit: int) -> Generator[Any, Any, None]:
        """
        列表生成器接口，每次生成一条数据
        :param limit: 取最新的条数
        :return: 抓取到的格式化list
        """
        for element in self.crawl(limit=limit):
            yield self.after(element)

    def __call__(self, limit: int) -> Generator[Any, Any, None]:
        return self.list(limit=limit)

    def crawl(self, limit: int) -> Generator[Any, str, None]:
        raise NotImplementedError

    def after(self, html: str) -> Any:
        raise NotImplementedError

    def sleep(self):
        time.sleep(random.uniform(self.half_interval / 2, self.interval))


class Analyzer(BaseAnalyzer):
    """
    分析器
    """

    def __init__(self, pagination: Pager, selector: Selector, interval: float = 0.1) -> None:
        """
        分析器
        :param pagination: 分页器(Pagination对象)
        :param selector: 抽取list的选择器(Selector对象)
        :param interval: 抓取list频率，可使用self.sleep()方法控制频率
        """
        super().__init__(interval)
        self.pagination: Pager = pagination
        self.selector: Selector = selector

    def crawl(self, limit: int) -> Generator[Any, str, None]:
        try:
            res_set = set()
            html = self.pagination.html
            if not html:
                return
            res: list[str] = self.selector(html)
            cnt = 0
            while cnt < len(res) and limit:  # 生成数据
                element = res[cnt]
                if element not in res_set:
                    res_set.add(element)
                    limit -= 1
                    yield element
                cnt += 1
            try_cnt = 3
            while len(res) > 0:
                self.sleep()
                self.pagination.next()
                html = self.pagination.html
                if not html:
                    return
                res = self.selector(html)
                flag = False
                cnt = 0
                while cnt < len(res) and limit:  # 生成数据
                    element = res[cnt]
                    if element not in res_set:
                        res_set.add(element)
                        limit -= 1
                        yield element
                    cnt += 1
                if not flag and not try_cnt:
                    return
                if not flag:
                    try_cnt -= 1
        except:
            return

    def after(self, html: str) -> str:
        return html


class AnalyzerPrettify(Analyzer):
    """
    Prettify html
    """

    filter_list = ["\n", "\r", "\t", "<br>", "<br/>", "</br>"]

    def after(self, html: str) -> str:
        # 去除html中无用信息
        result_list = []
        i = 0
        while i < len(html):
            flag = True
            for e in AnalyzerPrettify.filter_list:
                if html[i:i + len(e)] == e:
                    i += len(e)
                    flag = False
            flag2 = True
            while i < len(html) and html[i] == " ":
                flag2 = False
                i += 1
            if not flag2:
                i -= 1
            if flag:
                result_list.append(html[i])
                i += 1
        result = "".join(result_list)
        return result
