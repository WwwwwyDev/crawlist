---
description: Some cases help you better understand it
---

# 👾 demo

### StaticPager

#### StaticRedirectPager

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

#### StaticListRedirectPager

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

### **Dynamic**Pager

#### DynamicRedirectPager

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

#### **D**ynamicListRedirectPager

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

#### **D**ynamicScrollPager

```python
import crawlist as cl

if __name__ == '__main__':
    pager = cl.DynamicScrollPager(uri="https://ec.ltn.com.tw/list/international")
    selector = cl.CssSelector(pattern="#ec > div.content > section > div.whitecon.boxTitle.boxText > ul > li")
    analyzer = cl.AnalyzerLinks(pager=pager, selector=selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))
    pager.webdriver.quit()

```

#### **D**ynamicLineButtonPager

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

#### **D**ynamicNumButtonPager

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

#### **D**ynamicNextButtonPager

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

### Pre-loading

```python
from selenium.webdriver.remote.webdriver import WebDriver
import crawlist as cl

if __name__ == '__main__':
    class MyPager(cl.DynamicLineButtonPager):
        def pre_load(self, webdriver: WebDriver = None) -> None:
            webdriver.get("https://kuaixun.eastmoney.com/")
            cl.Action.click(webdriver, '/html/body/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/label/span[1]')
        
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

```python
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

import crawlist as cl

if __name__ == '__main__':
    button_selector = cl.CssWebElementSelector(pattern='#frs_list_pager > a')
    uri = "https://tieba.baidu.com/f?kw=%E8%B4%B4%E5%90%A7&ie=utf-8&pn=0"


    class MyPager(cl.DynamicNumButtonPager):
        def pre_load(self, webdriver: WebDriver = None) -> None:
            webdriver.get(uri)
            #  You also could use the selenium methods.
            element = webdriver.find_element(By.XPATH, xpath)
            element.click()

    pager = MyPager(uri=uri,
                    button_selector=button_selector)
    selector = cl.CssSelector(pattern='#thread_list > li')
    analyzer = cl.AnalyzerPrettify(pager=pager, selector=selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))
    pager.webdriver.quit()
```

### Pre-loading with scripts

```python
from selenium.webdriver.remote.webdriver import WebDriver
import crawlist as cl

if __name__ == '__main__':
    class MyPager(cl.DynamicNumButtonPager):
        def pre_load(self, webdriver: WebDriver) -> None:
            webdriver.get(baidu_uri)
            script = {
                "method": "inputKeyword",
                "xpath": '//*[@id="kw"]',
                "keyword": "和泉雾纱",
                "next": {
                    "method": "click",
                    "xpath": '//*[@id="su"]',
                }
            }  # You could save the script as Json on your physical storage
            cl.Script(script)(webdriver)

    pager = MyPager(uri=baidu_uri,
                    button_selector=cl.XpathWebElementSelector('//*[@id="page"]/div/a/span'),
                    webdriver=cl.DefaultDriver(isDebug=True), interval=5)
    selector = cl.XpathSelector(pattern='/html/body/div[3]/div[3]/div[1]/div[3]/div')
    analyzer = cl.AnalyzerPrettify(pager, selector)
    res = []
    for tr in analyzer(TestCase.limit):
        print(tr)
        res.append(tr)
    print(len(res))
    pager.webdriver.quit()
```

### Implement your own Request

```python
import requests
from requests import HTTPError

import crawlist as cl

if __name__ == '__main__':
    class MyRequest(cl.Request):
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


    pager = cl.StaticRedirectPager(uri="https://www.douban.com/doulist/893264/?start=0&sort=seq&playable=0&sub_type=",
                                   uri_split="https://www.douban.com/doulist/893264/?start=%v&sort=seq&playable=0&sub_type=",
                                   start=0,
                                   offset=25, request=MyRequest())
    selector = cl.CssSelector(pattern=".doulist-item")

    analyzer = cl.AnalyzerPrettify(pager, selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))

```

### Use your own webdriver

```python
import crawlist as cl
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver as wd
from selenium.webdriver.chrome.service import Service

if __name__ == '__main__':
    class MyDriver(cl.Driver):
        def __init__(self):
            pass

        def get_driver(self) -> WebDriver:
            option = wd.ChromeOptions()
            option.add_argument("start-maximized")
            option.add_argument("--headless")
            option.add_argument("window-size=1920x3000")
            agent = 'user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"'
            option.add_argument(agent)
            my_webdriver = wd.Chrome(service=Service(ChromeDriverManager().install()), options=option)
            return my_webdriver

    pager = cl.DynamicScrollPager(uri="https://ec.ltn.com.tw/list/international", webdriver=MyDriver())
    selector = cl.CssSelector(pattern="#ec > div.content > section > div.whitecon.boxTitle.boxText > ul > li")
    analyzer = cl.AnalyzerPrettify(pager=pager, selector=selector)
    res = []
    for tr in analyzer(TestCase.limit):
        print(tr)
        res.append(tr)
    print(len(res))
    pager.webdriver.quit()

```

