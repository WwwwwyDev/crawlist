import re
from cssselect.parser import SelectorError
from cssselect.xpath import HTMLTranslator
from lxml import etree


class Valid(object):

    uri_regex = re.compile(
        r'^(?:http|ftp)s?://'  # http或https或ftp或ftps
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # 域名
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP地址
        r'(?::\d+)?'  # 端口
        r'(?:/[^?#]*)?'  # 路径
        r'(?:\?[^#]+)?'  # 查询字符串
        r'(?:#.*)?$', re.IGNORECASE)

    @staticmethod
    def is_valid_url(uri: str) -> bool:
        return re.match(Valid.uri_regex, uri) is not None

    @staticmethod
    def is_valid_regex(pattern: str) -> bool:
        try:
            re.compile(pattern)
            return True
        except re.error:
            return False

    @staticmethod
    def is_valid_xpath(xpath: str) -> bool:
        try:
            etree.XPath(xpath)
            return True
        except etree.XPathSyntaxError:
            return False

    @staticmethod
    def is_valid_css(css: str) -> bool:
        try:
            HTMLTranslator().css_to_xpath(css)
            return True
        except SelectorError:
            return False
