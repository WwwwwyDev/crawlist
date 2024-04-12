---
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

# 📖 pager

Paginators are divided into static paginators and dynamic paginators. Static paginators can be used to handle non JS driven web pages, while dynamic paginators can be used to handle JS driven web pages. Generally speaking, web pages that static paginators can handle are usually paginated using redirection, and dynamic paginators can also handle them.

### type of pager

We have implemented 8 selectors, which are sufficient to handle most web pages.

```python
import crawlist as cl
# dynamic
cl.DynamicLineButtonPager(some args...)
cl.DynamicScrollPager(some args...)
cl.DynamicRedirectPager(some args...)
cl.DynamicListRedirectPager(some args...)
cl.DynamicNumButtonPager(some args...)
cl.DynamicNextButtonPager(some args...)
# static
cl.StaticRedirectPager(some args...)
cl.StaticListRedirectPager(some args...)
```

You can view their details in the sub sections.
