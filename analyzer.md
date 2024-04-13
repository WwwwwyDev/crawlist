---
description: Achieve linkage between pagers and selectors
---

# 👾 analyzer

```python
class Analyzer(BaseAnalyzer):

    def __init__(self, pager: Pager, selector: Selector) -> None:
        """
        Achieve linkage between pagers and selectors
        : param pager: Pager (Pager object or its subclass implementation)
        : param selector: Selector (Selector object or its subclass implementation)
        """
```

If you want to implement your own analyzer and format data output, you can refer to the following code.

```python
import crawlist as cl

class MyAnalyzer(cl.Analyzer):
    
    def after(self, html: str) -> Any:
        raise NotImplementedError
```

We also provide several built-in commonly used analyzers.

```python
import crawlist as cl
cl.AnalyzerPrettify(pager , selector)  # It will beautify your output HTML string
cl.AnalyzerLinks(pager , selector)  #  It will extract all the links
```
