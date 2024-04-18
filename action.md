---
description: >-
  We have built-in web page behaviors that make it easier for you to operate web
  pages.You may use the Action in the pre_load.
---

# 👾 action

### type of action

We have implemented 7 actions

<pre class="language-python"><code class="lang-python">import crawlist as cl
action = cl.Action
action.click(...args)
action.inputKeyword(...args)
action.sendEnter(...args)
<strong>action.switchLastTab(...args)
</strong>action.switchTab(...args)
action.searchRedirect(...args)
action.redirect(...args)
</code></pre>

### what is pre\_load？

The pre\_load is used in dynamic pager in order to process the webdriver before the analyzer works.

```python
import crawlist as cl
class MyPager(cl.DynamicLineButtonPager):
        def pre_load(self, webdriver: WebDriver = None) -> None:
            webdriver.get("https://kuaixun.eastmoney.com/")
            cl.Action.click(webdriver, '/html/body/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[3]/label/span[1]')

```

### parms of action



<table><thead><tr><th>methods</th><th>parms</th><th data-hidden></th></tr></thead><tbody><tr><td>click</td><td><p>driver – selenium webdriver </p><p>xpath – Click on the xpath path of the button</p></td><td></td></tr><tr><td>inputKeyword</td><td><p>driver – selenium webdriver </p><p>xpath – The xpath path of the input box keyword – keyword needs to be passed in</p></td><td></td></tr><tr><td>sendEnter</td><td><p>driver– selenium webdriver</p><p>xpath – The xpath path of the input box</p></td><td></td></tr><tr><td>switchLastTab</td><td>driver – selenium webdriver</td><td></td></tr><tr><td>switchTab</td><td><p>driver – selenium webdriver </p><p>index – The index handle</p></td><td></td></tr><tr><td>searchRedirect</td><td><p>driver – selenium webdriver </p><p>url – Link containing %s </p><p>keyword – keyword needs to be passed in</p></td><td></td></tr><tr><td>redirect</td><td><p>driver – selenium webdriver </p><p>url – Links that require redirection</p></td><td></td></tr></tbody></table>



