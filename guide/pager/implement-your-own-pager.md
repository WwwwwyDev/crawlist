---
description: realise
layout:
  title:
    visible: true
  description:
    visible: false
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# Implement your own pager

```python
import crawlist as cl

class MyPager(cl.Pager):

    def __init__(self, my_args, interval: float = 0.1):
        """
        :param interval: Grab the list frequency and adjust it according to the actual situation of the webpage
        """
        super().__init__(interval=interval)
        self.my_args = my_args

    def next(self) -> None:
        """
        Data Incremental Method
        :return:
        """
        raise NotImplementedError

    @property
    def html(self) -> str:
        """
        HTML text in the current state
        :return: The html text
        """
        raise NotImplementedError
```
