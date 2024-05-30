---
description: 实现翻页操作
layout:
  title:
    visible: true
  description:
    visible: true
  tableOfContents:
    visible: true
  outline:
    visible: true
  pagination:
    visible: true
---

# Pager

### 什么是 pager？

分页器分为静态分页器和动态分页器。静态分页器可以用于处理非JS驱动的网页，而动态分页器可以用来处理JS驱动的web页面。一般来说，静态分页器可以处理的网页通常使用重定向进行分页，动态分页器也可以处理它们。

### pager的种类

我们已经实现了8种pager，它们基本涵盖所有网页的分页方式

```python
import crawlist as cl
# 动态
cl.DynamicLineButtonPager(some args...)
cl.DynamicScrollPager(some args...)
cl.DynamicRedirectPager(some args...)
cl.DynamicListRedirectPager(some args...)
cl.DynamicNumButtonPager(some args...)
cl.DynamicNextButtonPager(some args...)
# 静态
cl.StaticRedirectPager(some args...)
cl.StaticListRedirectPager(some args...)
```
