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

# 概述

[<img src="https://s2.loli.net/2024/04/12/C9tV8wvzUPM7lgb.png" alt="crawlist" data-size="original">](https://github.com/WwwwwyDev/crawlist)

## crawlist

从web网站抓取列表数据的通用解决方案

[<img src="https://img.shields.io/pypi/v/crawlist" alt="pypi" data-size="line"> ](https://pypi.python.org/pypi/crawlist)<img src="https://img.shields.io/badge/python-3.10.0+-blue" alt="python" data-size="line">

{% embed url="https://github.com/WwwwwyDev/crawlist" %}

### 介绍

您可以使用crawlist对包含列表的网站进行数据爬取，通过一些简单的配置，您可以获得所有列表数据。

### 安装

你可以使用 pip 或者 pip3 来安装crawlist

`pip install crawlist` or `pip3 install crawlist`

如果你已经安装了crawlist，可能需要更新到最新版本

`pip install --upgrade crawlist`

### 快速开始

这是一个静态网站案例，该网站没有使用js去驱动视图

```python
import crawlist as cl

if __name__ == '__main__':
    # 初始化一个pager来实现翻页
    pager = cl.StaticRedirectPager(uri="https://www.douban.com/doulist/893264/?start=0&sort=seq&playable=0&sub_type=",
                                   uri_split="https://www.douban.com/doulist/893264/?start=%v&sort=seq&playable=0&sub_type=",
                                   start=0,
                                   offset=25) 
    
    # 初始化一个selector来爬取列表
    selector = cl.CssSelector(pattern=".doulist-item")
    
    # 初始化一个分析器，实现翻页+爬取列表
    analyzer = cl.AnalyzerPrettify(pager, selector)
    res = []
    limit = 100
    # 在分析器中迭代limit条数据
    for tr in analyzer(limit): 
        print(tr)
        res.append(tr)
    # 如果该网站所有数据都被抓取，则len(res)会小于limit
    print(len(res))
```

这是一个动态网站案例，它使用js去驱动视图，所以我们需要使用selenium去爬取

```python
import crawlist as cl

if __name__ == '__main__':
    # 初始化一个pager来实现翻页
    pager = cl.DynamicScrollPager(uri="https://ec.ltn.com.tw/list/international")
    
    # 初始化一个selector来爬取列表
    selector = cl.CssSelector(pattern="#ec > div.content > section > div.whitecon.boxTitle.boxText > ul > li")
    
    # 初始化一个分析器，实现翻页+爬取列表
    analyzer = cl.AnalyzerPrettify(pager=pager, selector=selector)
    res = []
    
    # 在分析器中迭代limit条数据
    limit = 100
    for tr in analyzer(limit):
        print(tr)
        res.append(tr)
    print(len(res))
    # 如果该网站所有数据都被抓取，则len(res)会小于limit
    pager.webdriver.quit()

```
