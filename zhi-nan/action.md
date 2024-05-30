---
description: crawlist内置了几个网页行为，使您更容易操作网页。您可以在pre_load中使用Action。
---

# Action

### action的种类

我们实现了7种action

```python
import crawlist as cl
action = cl.Action
action.click(...args)
action.inputKeyword(...args)
action.sendEnter(...args)
action.switchLastTab(...args)
action.switchTab(...args)
action.searchRedirect(...args)
action.redirect(...args)
```

### 什么是 pre\_load？

pre\_load用于动态翻页，以便在分析器工作之前进行网页交互。

```python
import crawlist as cl
class MyPager(cl.DynamicLineButtonPager):
        def pre_load(self, webdriver: WebDriver = None) -> None:
            webdriver.get("https://kuaixun.eastmoney.com/")
            cl.Action.click(webdriver, '/html/body/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/label/span[1]')

```

### action的参数

<table><thead><tr><th>methods</th><th>parms</th><th data-hidden></th></tr></thead><tbody><tr><td>click</td><td><p>driver – selenium webdriver </p><p>xpath – Click on the xpath path of the button</p></td><td></td></tr><tr><td>inputKeyword</td><td><p>driver – selenium webdriver </p><p>xpath – The xpath path of the input box keyword – keyword needs to be passed in</p></td><td></td></tr><tr><td>sendEnter</td><td><p>driver– selenium webdriver</p><p>xpath – The xpath path of the input box</p></td><td></td></tr><tr><td>switchLastTab</td><td>driver – selenium webdriver</td><td></td></tr><tr><td>switchTab</td><td><p>driver – selenium webdriver </p><p>index – The index handle</p></td><td></td></tr><tr><td>searchRedirect</td><td><p>driver – selenium webdriver </p><p>url – Link containing %s </p><p>keyword – keyword needs to be passed in</p></td><td></td></tr><tr><td>redirect</td><td><p>driver – selenium webdriver </p><p>url – Links that require redirection</p></td><td></td></tr></tbody></table>



