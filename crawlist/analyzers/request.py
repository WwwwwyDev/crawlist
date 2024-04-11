from requests import HTTPError
import requests


class BaseRequest(object):
    pass


class Request(BaseRequest):
    """
    http请求对象，如果需要重写，请继承Request对象
    """
    def __init__(self, headers=None, proxies=None):
        if proxies is None:
            proxies = {}
        if headers is None:
            headers = {}
        self.headers = headers
        self.proxies = proxies

    def request(self, uri: str) -> str:
        try:
            r = requests.get(uri, headers=self.headers, proxies=self.proxies)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except HTTPError:
            return ""

    def __call__(self, uri) -> str:
        return self.request(uri)

