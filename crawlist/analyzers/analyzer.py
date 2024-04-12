import traceback
from typing import Any, Generator
from .selector import Selector
from .pager import Pager


class BaseAnalyzer(object):
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

    def __call__(self, limit: int) -> Generator[Any, Any, None]:
        return self.list(limit=limit)

    def crawl(self, limit: int) -> Generator[Any, str, None]:
        raise NotImplementedError

    def after(self, html: str) -> Any:
        raise NotImplementedError


class Analyzer(BaseAnalyzer):
    """
    分析器
    """

    def __init__(self, pager: Pager, selector: Selector) -> None:
        """
        分析器
        :param pager: 分页器(Pagination对象)
        :param selector: 抽取list的选择器(Selector对象)
        """
        self.pager: Pager = pager
        self.selector: Selector = selector

    def crawl(self, limit: int) -> Generator[Any, str, None]:
        try:
            res_set = set()
            html = self.pager.html
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
            while len(res) > 0 and limit:
                self.pager.next()
                html = self.pager.html
                if not html:
                    return
                res = self.selector(html)
                flag = False
                cnt = 0
                while cnt < len(res) and limit:  # 生成数据
                    element = res[cnt]
                    if element not in res_set:
                        flag = True
                        res_set.add(element)
                        limit -= 1
                        yield element
                    cnt += 1
                if not flag and not try_cnt:
                    return
                if not flag:
                    try_cnt -= 1
        except:
            tb = traceback.format_exc()
            print(tb)
            return

    def after(self, html: str) -> str:
        return html


class AnalyzerPrettify(Analyzer):
    """
    分析器，美化输出
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
