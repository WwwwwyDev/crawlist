# crawlist
A universal solution for web crawling lists


### Pagination

#### NormalPagination
```python
import crawlist as cl

if __name__ == '__main__':
    request = cl.Request()
    pagination = cl.NormalPagination(request, uri="https://www.douban.com/doulist/893264/?start=0&sort=seq&playable=0&sub_type=",
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

#### NormalPaginationList
```python
import crawlist as cl

if __name__ == '__main__':
    request = cl.Request()
    uris = ["https://www.douban.com/doulist/893264/?start=0&sort=seq&playable=0&sub_type=",
            "https://www.douban.com/doulist/893264/?start=25&sort=seq&playable=0&sub_type=",
            "https://www.douban.com/doulist/893264/?start=50&sort=seq&playable=0&sub_type=",
            "https://www.douban.com/doulist/893264/?start=75&sort=seq&playable=0&sub_type="]
    pagination = cl.NormalPaginationList(request, uris=uris)
    selector = cl.CssSelector(pattern=".doulist-item")

    analyzer = cl.AnalyzerPrettify(pagination, selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))
```
#### AdvancedPaginationListRedirect
```python
import crawlist as cl
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    option.add_argument("start-maximized")
    option.add_argument("--headless")
    option.add_argument("window-size=1920x3000")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    uris = ["https://www.boc.cn/sourcedb/whpj/index.html",
            "https://www.boc.cn/sourcedb/whpj/index_1.html",
            "https://www.boc.cn/sourcedb/whpj/index_2.html",
            "https://www.boc.cn/sourcedb/whpj/index_3.html"]
    pagination = cl.AdvancedPaginationListRedirect(driver, uris=uris)
    selector = cl.CssSelector(pattern="body > div > div.BOC_main > div.publish > div:nth-child(3) > table > tbody > tr")

    analyzer = cl.AnalyzerPrettify(pagination, selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))
    driver.close()
```

#### AdvancedPaginationRedirect
```python
import crawlist as cl
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    option.add_argument("start-maximized")
    option.add_argument("--headless")
    option.add_argument("window-size=1920x3000")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=option)
    pagination = cl.AdvancedPaginationRedirect(driver, uri="https://www.boc.cn/sourcedb/whpj/index.html",
                                               uri_split="https://www.boc.cn/sourcedb/whpj/index_%v.html",
                                               start=0)
    selector = cl.CssSelector(pattern="body > div > div.BOC_main > div.publish > div:nth-child(3) > table > tbody > tr")

    analyzer = cl.AnalyzerPrettify(pagination, selector)
    res = []
    for tr in analyzer(100):
        print(tr)
        res.append(tr)
    print(len(res))
    driver.close()
```