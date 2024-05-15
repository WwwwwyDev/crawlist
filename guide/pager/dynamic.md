---
description: DynamicPager
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

# Dynamic

There are six types of implementation for dynamic paginators

<pre class="language-python"><code class="lang-python"><strong>class DynamicRedirectPager(DynamicPager):
</strong>    def __init__(self, uri: str, uri_split: str, webdriver: WebDriver = None, start: int = 1, offset: int = 1,
                 interval: float = 0.1) -> None:
        """
        Based on dynamic web page analyzer (redirect page flipping)
        :param uri: First page link
        :param uri_split: Link pagination (using %v proxy) Example: https://www.boc.cn/sourcedb/whpj/index_%v.html
        :param webdriver: WebDriver object for selenium
        :param start: Start page
        :param offset: pagination interval
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
</code></pre>

```python
class DynamicListRedirectPager(DynamicPager):
    def __init__(self, uris: list, webdriver: WebDriver = None, interval: float = 0.1) -> None:
        """
        Based on dynamic web page analyzer (redirect page flipping)
        :param uris: A list containing multiple uris, executed in order downwards
        :param webdriver: WebDriver object for selenium
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
```

```python
class DynamicScrollPager(DynamicPager):
    def __init__(self, uri: str, webdriver: WebDriver = None, interval: float = 1) -> None:
        """
        Based on dynamic web page analyzer (scrolling and flipping)
        :param uri: webpage link, which is a scrolling page
        :param webdriver: WebDriver object for selenium
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
```

```python
class DynamicLineButtonPager(DynamicPager):
    def __init__(self, uri: str, button_selector: WebElementSelector, webdriver: WebDriver = None,
                 interval: float = 1) -> None:
        """
        Based on dynamic web page analyzer (row button page flipping)
        :param uri: webpage link, which is a row button for flipping pages
        :param button.selector: row button selector
        :param webdriver: WebDriver object for selenium
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
```

```python
class DynamicNumButtonPager(DynamicPager):
    def __init__(self, uri: str, button_selector: WebElementSelector, webdriver: WebDriver = None, start: int = 1,
                 offset: int = 1, interval: float = 1) -> None:
        """
        Based on dynamic web page analyzer (digital button flipping)
        :param uri: webpage link, which is a numeric button for flipping pages
        :param button.selector: numeric button selector
        :param webdriver: WebDriver object for selenium
        :param start: Start page
        :param offset: pagination interval
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
```

```python
class DynamicNextButtonPager(DynamicPager):
    def __init__(self, uri: str, button_selector: WebElementSelector, webdriver: WebDriver = None, start: int = 1,
                 offset: int = 1, interval: float = 1) -> None:
        """
        Based on dynamic web page analyzer (click the next page button to page)
        :param uri: Web page link, which is a page that can be flipped by clicking the next page button
        :param button.selector: Click on the next page button selector
        :param webdriver: WebDriver object for selenium
        :param start: Start page
        :param offset: pagination interval
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
```
