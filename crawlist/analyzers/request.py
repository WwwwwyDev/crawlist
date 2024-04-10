from requests import HTTPError
import requests


class RequestBase(object):
    def request(self, uri) -> str:
        raise NotImplementedError

    def __call__(self, uri) -> str:
        return self.request(uri)


class Request(RequestBase):
    """
    http请求对象，如果需要重写，请继承Request对象
    """
    def request(self, uri) -> str:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/70.0.3538.77 Safari/537.36"
            }
            r = requests.get(uri, headers=headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except HTTPError:
            return ""

