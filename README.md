# crawlist
A universal solution for web crawling lists


## Pager

### StaticPager

#### StaticPagerRedirect

```python
import crawlist as cl

if __name__ == '__main__':
    pagination = cl.StaticPagerRedirect(uri="https://www.douban.com/doulist/893264/?start=0&sort=seq&playable=0&sub_type=",
                                        uri_split="https://www.douban.com/doulist/893264/?start=%v&sort=seq&playable=0&sub_type=",
                                        start=0,
                                        offset=25)
    selector = cl.CssSelector(pattern=".doulist-item")

    analyzer = cl.AnalyzerPrettify(pagination, selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))
```

#### StaticPagerListRedirect

```python
import crawlist as cl

if __name__ == '__main__':
    uris = ["https://www.douban.com/doulist/893264/?start=0&sort=seq&playable=0&sub_type=",
            "https://www.douban.com/doulist/893264/?start=25&sort=seq&playable=0&sub_type=",
            "https://www.douban.com/doulist/893264/?start=50&sort=seq&playable=0&sub_type=",
            "https://www.douban.com/doulist/893264/?start=75&sort=seq&playable=0&sub_type="]
    pagination = cl.StaticPagerListRedirect(uris=uris)
    selector = cl.CssSelector(pattern=".doulist-item")

    analyzer = cl.AnalyzerPrettify(pagination, selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))
```
#### DynamicPagerListRedirect

```python
import crawlist as cl

if __name__ == '__main__':
    uris = ["https://www.boc.cn/sourcedb/whpj/index.html",
            "https://www.boc.cn/sourcedb/whpj/index_1.html",
            "https://www.boc.cn/sourcedb/whpj/index_2.html",
            "https://www.boc.cn/sourcedb/whpj/index_3.html",
            "https://www.boc.cn/sourcedb/whpj/index_4.html"]
    pagination = cl.DynamicPagerListRedirect(uris=uris)
    selector = cl.CssSelector(pattern="body > div > div.BOC_main > div.publish > div:nth-child(3) > table > tbody > tr")

    analyzer = cl.AnalyzerPrettify(pagination, selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))
    pagination.webdriver.quit()

```

#### DynamicPagerRedirect

```python
import crawlist as cl

if __name__ == '__main__':
    pagination = cl.DynamicPagerRedirect(uri="https://www.boc.cn/sourcedb/whpj/index.html",
                                         uri_split="https://www.boc.cn/sourcedb/whpj/index_%v.html",
                                         start=0)
    selector = cl.CssSelector(pattern="body > div > div.BOC_main > div.publish > div:nth-child(3) > table > tbody > tr")

    analyzer = cl.AnalyzerPrettify(pagination, selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))
    pagination.webdriver.quit()

```