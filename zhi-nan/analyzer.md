---
description: 连接pager和selector
---

# Analyzer

```python
class Analyzer(BaseAnalyzer):

    def __init__(self, pager: Pager, selector: Selector) -> None:
        """
        Achieve linkage between pagers and selectors
        :param pager: Pager (Pager object or its subclass implementation)
        :param selector: Selector (Selector object or its subclass implementation)
        """
```

### 实现自己的analyzer

```python
import crawlist as cl

class MyAnalyzer(cl.Analyzer):
    
    def after(self, html: str) -> Any:
        raise NotImplementedError
```

我们也提供了两个内置的analyzer

```python
import crawlist as cl
cl.AnalyzerPrettify(pager , selector)  # 美化你的html
cl.AnalyzerLinks(pager , selector)  #  抽取html中所有链接
```
