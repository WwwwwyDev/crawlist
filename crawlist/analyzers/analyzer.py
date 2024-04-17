import re
import traceback
from typing import Any, Generator

from crawlist.analyzers.pager.pager import Pager
from crawlist.analyzers.selector import Selector
from crawlist.analyzers.trie import Trie
from crawlist.annotation import check


class BaseAnalyzer(object):
    """
    Analyzer interface, requires subclass method implementation
    """

    @check
    def list(self, limit: int) -> Generator[Any, Any, None]:
        """
        List generator interface, generating one data at a time
        :param limit: Take the latest number of entries
        :return: Captured formatted list
        """
        for element in self.crawl(limit=limit):
            yield self.after(element)

    @check
    def __call__(self, limit: int) -> Generator[Any, Any, None]:
        return self.list(limit=limit)

    def crawl(self, limit: int) -> Generator[Any, str, None]:
        raise NotImplementedError

    def after(self, html: str) -> Any:
        raise NotImplementedError


class Analyzer(BaseAnalyzer):

    def __init__(self, pager: Pager, selector: Selector) -> None:
        """
        Achieve linkage between pagers and selectors
        :param pager: Pager (Pager object or its subclass implementation)
        :param selector: Selector (Selector object or its subclass implementation)
        """
        self.pager: Pager = pager
        self.selector: Selector = selector

    def crawl(self, limit: int) -> Generator[Any, str, None]:
        try:
            res_set = Trie()
            html = self.pager.html
            if not html:
                return
            res: list[str] = self.selector(html)
            cnt = 0
            while cnt < len(res) and limit:  # Generate data
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
                while cnt < len(res) and limit:  # Generate data
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
    Analyzer, beautify output
    """

    filter_list = ["\n", "\r", "\t", "<br>", "<br/>", "</br>"]

    def after(self, html: str) -> str:
        # Remove useless information from HTML
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


class AnalyzerLinks(Analyzer):
    """
    Analyzer, extract all links
    """
    url_regex = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'

    def after(self, html: str) -> list:
        # Use regular expressions to find all matches
        links = re.findall(AnalyzerLinks.url_regex, html)
        return links
