import random
import time
import parsel


class Util:
    """
    util
    """

    # 选择html元素
    selector_rules = {"xpath", "css", "re"}
    @staticmethod
    def html_selector(html: str, rule: str, selector: str) -> list:
        """
        根据规则解析html文本内容
        :param html: html文本
        :param rule: 解析规则（"xpath", "css", "re"）
        :param selector: 选择器
        :return:
        """
        assert rule in Util.selector_rules
        html = Util.html_replace_str(html)  # 清洗html文本
        res = []
        if rule == "xpath":
            p_selector = parsel.Selector(text=html)
            res = p_selector.xpath(selector).getall()
        elif rule == "css":
            p_selector = parsel.Selector(text=html)
            res = p_selector.css(selector).getall()
        elif rule == "re":
            p_selector = parsel.Selector(text=html)
            res = p_selector.re(selector)
        return res

    @staticmethod
    def url_format(url: str, old_text, new_text: str) -> str:
        """
        替换url中的字符，主要是为了替换%v和%s
        :param url: url字符串
        :param old_text: 旧文本
        :param new_text: 新文本
        :return:
        """
        return url.replace(old_text, new_text)

    @staticmethod
    def random_sleep(start, end):
        """
        随机延时
        :param start: 范围左界
        :param end: 范围右界
        :return:
        """
        # 产生一个start到end之间的随机小数
        random_delay = random.uniform(start, end)
        # 延时,拟人行为
        time.sleep(random_delay)


    @staticmethod
    def html_replace_str(html: str) -> str:
        # 剔除无用信息
        html = html.replace("\n", '')
        html = html.replace("\r", '')
        html = html.replace("\t", '')
        html = html.replace("<br>", '')
        return html