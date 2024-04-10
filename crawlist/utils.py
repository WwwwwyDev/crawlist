import re
import parsel


class Util:
    """
    util
    """

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
    def html_replace_str(html: str) -> str:
        # 剔除无用信息
        html = html.replace("\n", '')
        html = html.replace("\r", '')
        html = html.replace("\t", '')
        html = html.replace("<br>", '')
        return html
