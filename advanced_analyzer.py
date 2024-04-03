from typing import Generator, Any

from analyzer_util import *
from analyzer import *
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec


# 基于selenium的分析器，用来分析动态网站
class AdvancedAnalyzer(Analyzer):
    """
    动态网页分析器，可以分析number;multi;line;scroll;redirect类型
    """

    def __init__(self, web_driver: WebDriver, analyzer_url: str, pagination_selector: str, pagination_type: str,
                 selector: str, rule: str = "xpath", pre_processing: callable = None, interval: float = 0.1,
                 start_page: int = 1, page_offset: int = 1, is_single_page: bool = False) -> None:
        """
        动态网页分析器，可以分析number;multi;line;scroll;redirect类型
        :param web_driver: selenium的webdriver驱动器
        :param analyzer_url: 需要爬取列表的url(第一页地址)
        :param pagination_selector: 分页器选择器(xpath语法)或分页链接地址，如果是分页链接(redirect类型)，分页处使用%v代替
        :param pagination_type: 分页器类型(number;multi;line;scroll;redirect)
        :param selector: 抽取list的选择题
        :param rule: 抽取规则(xpath, css, regExp, jsPath)
        :param pre_processing: 预操作回调函数
        :param interval: 切换下一页的间隔(根据网络情况调整)
        :param start_page: 起始页
        :param page_offset: 页面间隔
        :param is_single_page: 是否单页面抓取
        """
        super().__init__(analyzer_url=analyzer_url, selector=selector, rule=rule, interval=interval,
                         start_page=start_page, page_offset=page_offset, is_single_page=is_single_page)
        self.pagination_type_mp = {
            "number": self.type_num_button,
            "multi": self.type_next_page_button,
            "line": self.type_line_button,
            "scroll": self.type_scroll,
            "redirect": self.type_redirect
        }
        assert pagination_type in self.pagination_type_mp
        self.pagination_selector = pagination_selector
        self.driver = web_driver
        self.driver.get(analyzer_url)
        AnalyzerUtil.random_sleep(0.1, 0.3)  # 随机延迟
        # 预加载
        self.pre_processing = pre_processing
        if pre_processing:
            pre_processing(self.driver)
        AnalyzerUtil.random_sleep(0.1, 0.3)
        self.work_num = 1  # 记录第几次执行，如果多次执行list函数，则需要复原driver
        if pagination_type in {"line", "num"}:  # 如果是num和line类型，需要先检测一下分页器是否存在
            WebDriverWait(web_driver, self.interval).until(
                Ec.presence_of_element_located((By.XPATH, pagination_selector)))
            self.pagination = self.driver.find_elements(
                By.XPATH, pagination_selector)
        self.pagination_type = pagination_type
        self.is_single_page = is_single_page

    def refresh_driver(self) -> None:
        """
        复原driver
        """
        self.driver.get(self.analyzer_url)
        AnalyzerUtil.random_sleep(0.1, 0.3)
        # 预加载
        if self.pre_processing:
            self.pre_processing(self.driver)
        AnalyzerUtil.random_sleep(0.1, 0.3)

    def list(self, limit: int) -> Generator[Any, str, None]:
        """
        列表生成器，每次生成一条数据
        :param limit: 取最新的条数
        :return: 抓取到的list标签html文本
        """
        if self.work_num > 1:  # 如果第n次(n>1)执行list函数，则需要复原driver
            self.refresh_driver()  # 复原driver
            AnalyzerUtil.random_sleep(0.1, 0.3)
        if self.pagination_type in self.pagination_type_mp:
            for element in self.pagination_type_mp[self.pagination_type](limit):
                yield element
        self.work_num += 1  # 执行完后，执行次数+1

    def find_next_page_button(self, selector: str = "") -> WebElement | None:
        """
        尝试寻找下一页按钮
        :param selector: 下一页按钮的选择器，如果为空，则自动全局检索
        :return: 下一页按钮元素
        """
        # 寻找下一页按钮
        if not selector:  # 如果没有选择器，则全局查找可能的li和a标签，判断里面的文本是否包含下一页关键词（卫语句）
            next_button_element = None
            next_button_element_like = self.driver.find_elements(
                By.TAG_NAME, "a")
            for element in next_button_element_like:
                if AnalyzerUtil.judge_next_page_button(element.text):
                    next_button_element = element
                    break
            if not next_button_element:
                next_button_element_like = self.driver.find_elements(
                    By.TAG_NAME, "li")
                for element in next_button_element_like:
                    if AnalyzerUtil.judge_next_page_button(element.text):
                        next_button_element = element
                        break
            return next_button_element
        # 如果"|"在选择器，则在多个选择器中进行寻找
        if "|" in selector:
            selector_list = selector.split("|")
            for selector_element in selector_list:
                try:
                    next_button_element_like = self.driver.find_elements(
                        By.XPATH, selector_element)
                    if len(next_button_element_like) == 1:
                        return next_button_element_like[0]
                except Exception:
                    pass
        else:
            # 如果有选择器，直接根据选择器选中下一页按钮
            try:
                next_button_element_like = self.driver.find_elements(
                    By.XPATH, selector)
                if len(next_button_element_like) == 1:
                    return next_button_element_like[0]
            except Exception:
                pass

        # 如果还是没有找到下一页按钮，则根据tag的名称尝试检索
        try:
            next_button_element_like = self.driver.find_elements(
                By.TAG_NAME, selector)
            for element in next_button_element_like:
                if AnalyzerUtil.judge_next_page_button(element.text):
                    return element
        except Exception:
            pass

        # 如果还是没有找到下一页按钮，则根据css规则尝试检索
        try:
            next_button_element_like = self.driver.find_elements(
                By.CSS_SELECTOR, selector)
            for element in next_button_element_like:
                if AnalyzerUtil.judge_next_page_button(element.text):
                    return element
        except Exception:
            pass

        # 如果都没有找到，则返回None
        return None

    def type_next_page_button(self, limit) -> Generator[Any, str, None]:
        """
        通过检索下一页按钮来进行翻页
        :param limit: 抓取最新的条数
        :return: 字符串生成器
        """
        next_button_element = self.find_next_page_button(
            self.pagination_selector)  # 寻找下一页按钮
        if not next_button_element:
            raise Exception("未检索到下一页按钮")
        while limit:
            current_page_html: str = self.driver.page_source
            current_page_res: list = AnalyzerUtil.html_selector(
                current_page_html, self.rule, self.selector)
            if len(current_page_res) == 0:  # 已经到最后一页
                self.is_max = True
                return
            cnt = 0
            while cnt < len(current_page_res) and limit:
                limit -= 1
                yield current_page_res[cnt]
                cnt += 1
            if self.is_single_page:
                return
            offset = self.page_offset
            while offset:  # offset为点击下一页的次数
                next_button_element = self.find_next_page_button(
                    self.pagination_selector)
                if not next_button_element:  # 已经到最后一页
                    self.is_max = True
                    return
                self.click_safety(next_button_element)
                AnalyzerUtil.random_sleep(
                    0.3 + self.interval, 0.5 + self.interval)
                offset -= 1

    @staticmethod
    def check_num_button(element: WebElement, num: int = 1) -> bool:
        """
        查找元素的inner_text中是否有数字
        :param element: selenium WebElement
        :param num: 判断的具体数字
        :return: 是否有数字
        """
        html = element.text
        inner_text = AnalyzerUtil.get_inner_text(html)
        return str(num) in inner_text

    @staticmethod
    def find_num_button(elements: List[WebElement], num: int = 1) -> WebElement | None:
        """
        在一组元素中，寻找符合条件的元素
        :param elements: selenium WebElement列表
        :param num: 需要的数字
        :return: 选中的按钮，没找到则为None
        """
        for element in elements:
            if AdvancedAnalyzer.check_num_button(element, num):
                return element
        return None

    def click_safety(self, button: WebElement) -> None:
        """
        尝试多次点击按钮
        :param button: 按钮元素
        """
        # 点击失败后多次尝试点击
        for _ in range(3):
            try:
                button.click()
                AnalyzerUtil.random_sleep(0.3 + self.interval, 0.5 + self.interval)
                break
            except Exception:
                pass

    def type_num_button(self, limit) -> Generator[Any, str, None]:
        """
        通过检索数字按钮来进行翻页
        :param limit: 抓取最新的条数
        :return: 字符串生成器
        """
        current_page_index = self.start_page
        while limit:
            current_page_html = self.driver.page_source
            current_page_res = AnalyzerUtil.html_selector(
                current_page_html, self.rule, self.selector)
            if len(current_page_res) == 0:  # 已经到最后一页
                self.is_max = True
                return
            cnt = 0
            while cnt < len(current_page_res) and limit:
                limit -= 1
                yield current_page_res[cnt]
                cnt += 1
            if self.is_single_page:  # 如果是单页抓取，则抓完一页直接返回
                return
            offset = self.page_offset
            while offset:  # offset为点击下一页的次数
                current_page_index += 1
                WebDriverWait(self.driver, self.interval).until(
                    Ec.presence_of_element_located((By.XPATH, self.pagination_selector)))  # 等待元素加载完成
                pagination = self.driver.find_elements(
                    By.XPATH, self.pagination_selector)
                button = AdvancedAnalyzer.find_num_button(
                    pagination, current_page_index)
                if not button:
                    self.is_max = True
                    return
                self.click_safety(button)
                AnalyzerUtil.random_sleep(
                    0.3 + self.interval, 0.5 + self.interval)
                offset -= 1

    def type_line_button(self, limit) -> Generator[Any, str, None]:
        """
        通过一行内点击类似“加载更多”按钮来进行翻页
        :param limit: 抓取最新的条数
        :return: 字符串生成器
        """
        WebDriverWait(self.driver, self.interval).until(
            Ec.presence_of_element_located((By.XPATH, self.pagination_selector)))  # 等待元素加载完成
        pagination = self.driver.find_elements(
            By.XPATH, self.pagination_selector)
        button = pagination[0]
        button.click()
        current_page_html = self.driver.page_source
        current_page_res = AnalyzerUtil.html_selector(
            current_page_html, self.rule, self.selector)
        if self.is_single_page:
            for element in current_page_res:
                yield element
            return
        pre_len = len(current_page_res)
        while len(current_page_res) < limit:  # 如果当前页面的list条数已经符合要求，则结束循环
            WebDriverWait(self.driver, self.interval).until(
                Ec.presence_of_element_located((By.XPATH, self.pagination_selector)))
            pagination = self.driver.find_elements(
                By.XPATH, self.pagination_selector)
            button = pagination[0]
            self.click_safety(button)
            AnalyzerUtil.random_sleep(0.3 + self.interval, 0.5 + self.interval)
            current_page_html = self.driver.page_source
            current_page_res = AnalyzerUtil.html_selector(
                current_page_html, self.rule, self.selector)
            # 检测是否到底部
            if pre_len >= len(current_page_res):
                limit = len(current_page_res)
                self.is_max = True
                break
            pre_len = len(current_page_res)
        for i in range(limit):
            yield current_page_res[i]

    def type_scroll(self, limit) -> Generator[Any, str, None]:
        """
        通过滚动进行翻页
        :param limit: 抓取最新的条数
        :return: 字符串生成器
        """
        js_code = '''he = setInterval(() => {
                        document.documentElement.scrollTop += document.documentElement.scrollHeight
                        if (document.documentElement.scrollTop >= (document.documentElement.scrollHeight - document.docu
                        mentElement.scrollWidth)) {
                            clearInterval(he)
                        }
                    },100)
                '''
        current_page_html = self.driver.page_source
        current_page_res = AnalyzerUtil.html_selector(
            current_page_html, self.rule, self.selector)
        if self.is_single_page:
            for element in current_page_res:
                yield element
            return
        len_record = set()
        while len(current_page_res) < limit:
            self.driver.execute_script(js_code)
            AnalyzerUtil.random_sleep(0.3 + self.interval, 0.5 + self.interval)
            current_page_html = self.driver.page_source
            current_page_res = AnalyzerUtil.html_selector(
                current_page_html, self.rule, self.selector)
            if len(current_page_res) in len_record:
                try_cnt = 5
                # 如果滚动到底部，继续尝试五次，还是没发生变化，就认为已经没有数据了
                while try_cnt and (len(current_page_res) in len_record):
                    try_cnt -= 1
                    self.driver.execute_script(js_code)  # 执行js脚本
                    AnalyzerUtil.random_sleep(
                        0.3 + self.interval, 0.5 + self.interval)
                    current_page_html = self.driver.page_source
                    current_page_res = AnalyzerUtil.html_selector(
                        current_page_html, self.rule, self.selector)
                if not try_cnt:
                    self.is_max = True
                    break
            len_record.add(len(current_page_res))
        for i in range(min(limit, len(current_page_res))):
            yield current_page_res[i]

    def type_redirect(self, limit) -> Generator[Any, str, None]:
        """
        通过重定向进行翻页
        :param limit: 抓取最新的条数
        :return: 字符串生成器
        """
        start_page_index = self.start_page
        # 第一页按照analyzer_html单独执行
        start_page_html = self.driver.page_source
        start_page_res = AnalyzerUtil.html_selector(
            start_page_html, self.rule, self.selector)
        cnt = 0
        while cnt < len(start_page_res) and limit:
            limit -= 1
            yield start_page_res[cnt]
            cnt += 1
        if self.is_single_page:  # 如果是单页爬取，则直接返回
            return
        # 从第二页开始循环
        start_page_index += self.page_offset
        while limit:
            cnt = 0
            self.driver.get(AnalyzerUtil.url_format(
                self.pagination_selector, r"%v", str(start_page_index)))
            current_page_html = self.driver.page_source
            current_page_res = AnalyzerUtil.html_selector(
                current_page_html, self.rule, self.selector)
            # 检测最后一页
            if len(current_page_res) == 0:
                self.is_max = True
                return
            while cnt < len(current_page_res) and limit:
                limit -= 1
                yield current_page_res[cnt]
                cnt += 1
            start_page_index += self.page_offset
