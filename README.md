# crawlist
A universal solution for web crawling lists


## Pager

### StaticPager

#### StaticPagerRedirect

```python
import crawlist as cl

if __name__ == '__main__':
    pager = cl.StaticRedirectPager(uri="https://www.douban.com/doulist/893264/?start=0&sort=seq&playable=0&sub_type=",
                                   uri_split="https://www.douban.com/doulist/893264/?start=%v&sort=seq&playable=0&sub_type=",
                                   start=0,
                                   offset=25)
    selector = cl.CssSelector(pattern=".doulist-item")

    analyzer = cl.AnalyzerPrettify(pager, selector)
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
    pager = cl.StaticListRedirectPager(uris=uris)
    selector = cl.CssSelector(pattern=".doulist-item")

    analyzer = cl.AnalyzerPrettify(pager, selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))
```


#### DynamicPagerRedirect

```python
import crawlist as cl

if __name__ == '__main__':
    pager = cl.DynamicRedirectPager(uri="https://www.boc.cn/sourcedb/whpj/index.html",
                                    uri_split="https://www.boc.cn/sourcedb/whpj/index_%v.html",
                                    start=0)
    selector = cl.CssSelector(pattern="body > div > div.BOC_main > div.publish > div:nth-child(3) > table > tbody > tr")

    analyzer = cl.AnalyzerPrettify(pager, selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))
    pager.webdriver.quit()

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
    pager = cl.DynamicListRedirectPager(uris=uris)
    selector = cl.CssSelector(pattern="body > div > div.BOC_main > div.publish > div:nth-child(3) > table > tbody > tr")

    analyzer = cl.AnalyzerPrettify(pager, selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))
    pager.webdriver.quit()

```

#### DynamicPagerScroll

```python
import crawlist as cl

if __name__ == '__main__':
    pager = cl.DynamicScrollPager(uri="https://ec.ltn.com.tw/list/international")
    selector = cl.CssSelector(pattern="#ec > div.content > section > div.whitecon.boxTitle.boxText > ul > li")
    analyzer = cl.AnalyzerPrettify(pager=pager, selector=selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))
    pager.webdriver.quit()

```
#### DynamicPagerLineButton

```python
import crawlist as cl

if __name__ == '__main__':
    button_selector = cl.CssWebElementSelector(pattern='#newslist > button')
    pager = cl.DynamicLineButtonPager(uri="https://www.yicai.com/news/kechuang/",
                                      button_selector=button_selector)
    selector = cl.XpathSelector(pattern='//*[@id="newslist"]/a')
    analyzer = cl.AnalyzerPrettify(pager=pager, selector=selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))
    pager.webdriver.quit()
```

#### DynamicPagerNumButton

```python
import crawlist as cl

if __name__ == '__main__':
    button_selector = cl.CssWebElementSelector(pattern='#kkpager > div:nth-child(1) > span.pageBtnWrap > a')
    pager = cl.DynamicNumButtonPager(uri="https://pccz.court.gov.cn/pcajxxw/gkaj/gkaj",
                                     button_selector=button_selector)
    selector = cl.CssSelector(pattern='#gkajlb ul')
    analyzer = cl.AnalyzerPrettify(pager=pager, selector=selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))
    pager.webdriver.quit()

```
#### DynamicNextButtonPager
```python
import crawlist as cl

if __name__ == '__main__':
    button_selector = cl.CssWebElementSelector(pattern='#downpage')
    pager = cl.DynamicNextButtonPager(uri="https://news.lnd.com.cn/xwyw/index.shtml",
                                      button_selector=button_selector, start=2, offset=2)
    selector = cl.CssSelector(
        pattern='body > div:nth-child(5) > div:nth-child(2) > div:nth-child(1) > div.main_more > span > ul > li')
    analyzer = cl.AnalyzerPrettify(pager=pager, selector=selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))
    pager.webdriver.quit()

```

### pre_load

```python
from selenium.webdriver.remote.webdriver import WebDriver

import crawlist as cl

if __name__ == '__main__':
    class MyPager(cl.DynamicLineButtonPager):
        def pre_load(self, webdriver: WebDriver = None) -> bool:
            webdriver.get("https://kuaixun.eastmoney.com/")
            cl.Action.click(webdriver, '/html/body/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/label/span[1]')
            return True
        
    pager = MyPager(uri="https://kuaixun.eastmoney.com/",
                                      button_selector=cl.CssWebElementSelector('#news_list > div.load_more'))
    selector = cl.CssSelector(pattern="#news_item_collection > div")

    analyzer = cl.AnalyzerPrettify(pager, selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))

```