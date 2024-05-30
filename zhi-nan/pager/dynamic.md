---
description: 动态pager
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

实现了六种动态分页方式

### 网页重定向

使用重定向方式翻页，链接中带有页码信息，将页码信息替换成%v后翻页器会自动将页码填入，实现翻页

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

### 网页列表重定向

将一组网页地址存入列表中，分页器直接按照列表前后顺序来翻页

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

### 滚动翻页

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

### 点击行下一页按钮

<figure><img src="../../.gitbook/assets/截屏2024-05-15 15.13.38.png" alt=""><figcaption></figcaption></figure>

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

### 数字翻页

<figure><img src="../../.gitbook/assets/截屏2024-05-15 15.14.31.png" alt=""><figcaption></figcaption></figure>

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

### 点击下一页按钮

<figure><img src="../../.gitbook/assets/截屏2024-05-15 15.15.49.png" alt=""><figcaption></figcaption></figure>

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
