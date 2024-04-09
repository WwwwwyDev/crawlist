from typing import Generator, Any

from analyzer import *
from crawlist.utils import *


class NormalAnalyzer(Analyzer):
    """
    静态网页分析器，可以分析链接分页网页
    example: https://www.boc.cn/sourcedb/whpj/index_%v.html
    """

    def __init__(self, analyzer_url: str, page_split_url: str, selector: str, rule: str = "xpath", interval: float = 0.1
                 , start_page: int = 1, page_offset: int = 1, is_single_page: bool = False) -> None:
        """
        静态网页分析器，可以分析链接分页网页
        example: https://www.boc.cn/sourcedb/whpj/index_%v.html
        :param analyzer_url: 需要爬取列表的url(第一页地址)
        :param page_split_url: 分页链接地址，分页处使用%v代替
        :param selector: 抽取list的选择题
        :param rule: 抽取规则(xpath, css, regExp, jsPath)
        :param start_page: 起始页
        :param page_offset: 页面间隔
        :param is_single_page: 是否单页面抓取
        """
        super().__init__(analyzer_url=analyzer_url, selector=selector, rule=rule, interval=interval,
                         start_page=start_page, page_offset=page_offset, is_single_page=is_single_page)
        self.page_split_url = page_split_url
        self.analyzer_html = AnalyzerUtil.get_html(analyzer_url)  # 根据url获取html文本
        self.is_single_page = is_single_page

    def list(self, limit: int) -> Generator[Any, str, None]:
        """
        列表生成器，每次生成一条数据
        :param limit: 取最新的条数
        :return: 抓取到的list标签html文本
        """
        for element in self.work(limit):
            yield element

    def work(self, limit) -> Generator[Any, str, None]:
        # 第一页按照analyzer_html单独执行
        page_index = self.start_page
        start_page_res = AnalyzerUtil.html_selector(self.analyzer_html, self.rule, self.selector)  # 根据文本从当前网页html
        # 文本中抓取所有符合条件的list元素
        cnt = 0
        while cnt < len(start_page_res) and limit:  # 生成数据
            limit -= 1
            yield start_page_res[cnt]
            cnt += 1
        if self.is_single_page:  # 如果是单页抓取，停止生成器
            return
        # 从第二页开始循环
        page_index += self.page_offset
        while limit:  # 当limit == 0 时停止while循环
            cnt = 0
            current_page_html = AnalyzerUtil.get_html(
                AnalyzerUtil.url_format(self.page_split_url, r"%v", str(page_index)))
            current_page_res: list = AnalyzerUtil.html_selector(
                current_page_html, self.rule, self.selector)
            if len(current_page_res) == 0:  # 检测最后一页，停止生成器
                self.is_max = True  # 修改is_max属性，标记已抓到最后一页
                return
            while cnt < len(current_page_res) and limit:  # 生成数据
                limit -= 1
                yield current_page_res[cnt]
                cnt += 1
            page_index += self.page_offset
            AnalyzerUtil.random_sleep(0 + self.interval, 0.2 + self.interval)
