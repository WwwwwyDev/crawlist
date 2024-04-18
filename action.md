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



<table><thead><tr><th>methods</th><th>parms</th><th data-hidden></th></tr></thead><tbody><tr><td></td><td>:param driver: selenium webdriver :param xpath: Click on the xpath path of the button</td><td></td></tr><tr><td></td><td></td><td></td></tr><tr><td></td><td></td><td></td></tr></tbody></table>



