---
description: 静态pager
layout:
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# Static

实现了两种静态分页方式

### 网页重定向

使用重定向方式翻页，链接中带有页码信息，将页码信息替换成%v后翻页器会自动将页码填入，实现翻页

```python
class StaticRedirectPager(StaticPager):
    def __init__(self, uri: str, uri_split: str, request: Request = None, start: int = 1, offset: int = 1,
                 interval: float = 0.1) -> None:
        """
        Based on static web page analyzer (redirect page flipping)
        :param uri_split: Link pagination (using %v instead) Example: https://www.boc.cn/sourcedb/whpj/index_%v.html
        :param uri: If set, It will be the First page link.
        :param request: Request object
        :param start: Start page
        :param offset: pagination interval
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
```

### 网页列表重定向

将一组网页地址存入列表中，分页器直接按照列表前后顺序来翻页

```python
class StaticListRedirectPager(StaticPager):
    def __init__(self, uris: list, request: Request = None, interval: float = 0.1) -> None:
        """
        Based on static web page analyzer (redirect page flipping)
        :param uris: A list containing multiple uris, executed in order downwards
        :param request: Request object
        :param interval: Grab the list frequency, which can be controlled using the self. sleep() method
        """
```
