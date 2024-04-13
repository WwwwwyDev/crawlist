---
description: StaticPager
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

# 👾 static

There are two types of implementation for static paginators

```python
class StaticRedirectPager(StaticPager):
    def __init__(self, uri: str, uri_split: str, request: Request = None, start: int = 1, offset: int = 1,
                 interval: float = 0.1) -> None:
        """
        Based on static web page analyzer (redirect page flipping)
        : param uri: First page link
        : param uri_split: Link pagination (using %v instead) Example: https://www.boc.cn/sourcedb/whpj/index_%v.html
        : param request: Request object
        : param start: Start page
        : param offset: pagination interval
        : param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
```

```python
class StaticListRedirectPager(StaticPager):
    def __init__(self, uris: list, request: Request = None, interval: float = 0.1) -> None:
        """
        Based on static web page analyzer (redirect page flipping)
        : param uris: A list containing multiple uris, executed in order downwards
        : param request: Request object
        : param interval: Grab the list frequency, which can be controlled using the self. sleep() method
        """
```
