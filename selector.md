---
description: choose the html element
---

# 🤞 selector

### what is selector?

The purpose of designing a selector is to distinguish various methods of selecting HTML elements (xpath, CSS, regex). We will use a selector to select the list elements in the HTML. Of course, we also need to use selectors to select the WebElement of selenium, so that the framework can operate on click events. If you don't know what selenium is, please learn it first.

### type of selector

```python
import crawlist as cl
# These selectors are designed to select list elements from web page text
css_selector = cl.CssSelector('your css')
xpath_selector = cl.XpathSelector('your xpath')
regex_selector = cl.RegexSelector('your regex')

# These selectors are designed to select the buttons in the webpage that involve data increment
css_webe_selector = cl.CssWebElementSelector('the button css')
xpath_webe_selector = cl.XpathWebElementSelector('the button xpath')
```

### How to implement your own selector

I think the above selectors are sufficient for use, but if you still want to implement your own selector, you can follow the following code to do it.

```python
import crawlist as cl

class MySelector(cl.Selector):
    
    # You need to rewrite the select() and valid() methods.
    # The select method needs to select the list you need from the HTML text.
    def select(self, html: str) -> list[str]:
        pattern = self.pattern
        raise NotImplementedError
    # The purpose of the valid method is to verify your pattern, and you can also ignore it.
    def valid(self, pattern) -> bool:
        raise NotImplementedError
```
