from requests import HTTPError
import requests


class BaseRequest(object):
    pass


class Request(BaseRequest):
    """
    HTTP request object, if it needs to be rewritten, please inherit the Request object
    """

    def request(self, uri: str) -> str:
        raise NotImplementedError

    def __call__(self, uri) -> str:
        return self.request(uri)


class DefaultRequest(Request):

    def request(self, uri: str) -> str:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
                'Cache-Control': 'max-age=0',
            }
            r = requests.get(uri, headers=headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except HTTPError:
            return ""
