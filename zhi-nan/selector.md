---
description: 选择html列表元素
---

# Selector

### 什么是 selector？

设计选择器的目的是区分选择HTML元素（xpath、css、regex）的各种方法。我们将使用选择器来选择HTML中的列表元素。当然，我们还需要使用选择器来选择selenium的WebElement，这样crawlist就可以对下一页的点击事件进行操作。如果你不知道selenium是什么，请先学一下。

{% embed url="https://www.selenium.dev/" %}

### 什么是列表元素？

红框内的内容，即为一个列表元素

<figure><img src="../.gitbook/assets/截屏2024-05-15 14.47.46.png" alt=""><figcaption></figcaption></figure>

### selector

```python
import crawlist as cl
# 从web网页文本中选择对应列表元素
css_selector = cl.CssSelector('your css')
xpath_selector = cl.XpathSelector('your xpath')
regex_selector = cl.RegexSelector('your regex')

# 选择selenium的webElement选择，在动态的pager中使用
css_webe_selector = cl.CssWebElementSelector('the button css')
xpath_webe_selector = cl.XpathWebElementSelector('the button xpath')
```

### 实现你自己的选择器

如果你想要实现自己的选择器，可以参考如下代码

```python
import crawlist as cl

# 继承自cl.Selector类
class MySelector(cl.Selector):
    
    # 你需要重写select和valid方法
    # 在当前html中选择出你需要的内容，并将它们组合成列表返回
    def select(self, html: str) -> list[str]:
        pattern = self.pattern # 规则
        raise NotImplementedError
    # 校验你的规则，可以忽略
    def valid(self, pattern) -> bool:
        raise NotImplementedError
```
