---
description: A universal solution for web crawling lists
layout:
  title:
    visible: false
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# 👾 home

[<img src="https://s2.loli.net/2024/04/12/C9tV8wvzUPM7lgb.png" alt="crawlist" data-size="original">](https://github.com/WwwwwyDev/crawlist)

## crawlist

A universal solution for web crawling lists

[<img src="https://img.shields.io/pypi/v/crawlist" alt="pypi" data-size="line"> ](https://pypi.python.org/pypi/crawlist)<img src="https://img.shields.io/badge/python-3.6.0+-blue" alt="python" data-size="line">

{% embed url="https://github.com/WwwwwyDev/crawlist" %}

### introduction

You can use Crawlist to crawl websites containing lists, and with some simple configurations, you can obtain all the list data.\
Of course, in the face of some special websites that cannot be crawled, you can also customize the configuration of that website.

### installing

You can use pip or pip3 to install the crawlist\
`pip install crawlist` or `pip3 install crawlist`

### quickly start

This is a static website demo. It does not use the JavaScript to load the data.

```python
import crawlist as cl

if __name__ == '__main__':
    # Initialize a pager to implement page flipping 
    pager = cl.StaticRedirectPager(uri="https://www.douban.com/doulist/893264/?start=0&sort=seq&playable=0&sub_type=",
                                   uri_split="https://www.douban.com/doulist/893264/?start=%v&sort=seq&playable=0&sub_type=",
                                   start=0,
                                   offset=25) 
    
    # Initialize a selector to select the list element
    selector = cl.CssSelector(pattern=".doulist-item")
    
    # Initialize an analyzer to achieve linkage between pagers and selectors
    analyzer = cl.AnalyzerPrettify(pager, selector)
    res = []
    limit = 100
    # Iterating a certain number of results from the analyzer
    for tr in analyzer(limit): 
        print(tr)
        res.append(tr)
    # If all the data has been collected, the length of the result will be less than the limit
    print(len(res))
```

This is a dynamic website demo. It uses the JavaScript to load the data.So we need to load a selenium webdriver to drive the JavaScript.

```python
import crawlist as cl

if __name__ == '__main__':
    # Initialize a pager to implement page flipping 
    pager = cl.DynamicScrollPager(uri="https://ec.ltn.com.tw/list/international")
    
    # Initialize a selector to select the list element
    selector = cl.CssSelector(pattern="#ec > div.content > section > div.whitecon.boxTitle.boxText > ul > li")
    
    # Initialize an analyzer to achieve linkage between pagers and selectors
    analyzer = cl.AnalyzerPrettify(pager=pager, selector=selector)
    res = []
    
    # Iterating a certain number of results from the analyzer
    limit = 100
    for tr in analyzer(limit):
        print(tr)
        res.append(tr)
    print(len(res))
    # After completion, you need to close the webdriver, otherwise it will occupy your memory resources
    pager.webdriver.quit()

```
