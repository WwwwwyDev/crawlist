# 分析器父类对象，需要子类实现
class Analyzer:
    """
    分析器接口,需要子类方法实现
    """

    def __init__(self, analyzer_url: str, selector: str, rule: str = "xpath", interval: float = 0.1, start_page: int = 1, page_offset: int = 1,
                 is_single_page: bool = False) -> None:
        """
        分析器接口,需要子类方法实现
        :param analyzer_url: 需要爬取列表的url
        :param selector: 抽取list的选择题
        :param rule: 抽取规则(xpath, css, regExp, jsPath)
        :param start_page: 起始页
        :param page_offset: 页面间隔
        :param is_single_page: 是否单页读取
        """
        assert rule in {"xpath", "css", "regExp", "jsPath"}
        self.analyzer_url = analyzer_url
        self.start_page = start_page
        self.page_offset = page_offset
        self.rule = rule
        self.interval = interval
        self.selector = selector
        self.is_max = False  # 是否已到最后一页
        self.is_single_page = is_single_page

    def list(self, limit: int):
        """
        列表生成器接口，每次生成一条数据
        :param limit: 取最新的条数
        :return: 抓取到的list标签html文本
        """
        raise NotImplementedError
