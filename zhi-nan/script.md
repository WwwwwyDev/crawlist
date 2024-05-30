---
description: 通过使用内置脚本，您可以更好地操作selenium的网络驱动程序。它还可以方便您将脚本存储在数据库等物理存储中，以便更快地进行调整。
---

# Script

### Script 定义

该脚本是一个JSON字符串。JSON可以用大多数语言进行解析，使其更加通用。嵌套多个JSON以实现连续操作。

#### 样例

```json
 {
	"method": "redirect",
	"url": "https://www.baidu.com/",
	"next": {
		"method": "inputKeyword",
		"xpath": "//*[@id=\"kw\"]",
		"keyword": "和泉雾纱",
		"next": {
			"method": "click",
			"xpath": "//*[@id=\"su\"]"
		}
	}
}
```

方法及其参数对应于所有[action](action.md#parms-of-action)名称及其参数

### 使用

更建议您在[pre\_load](action.md#what-is-pre\_load)中使用脚本。

```python
import crawlist as cl

class MyPager(cl.DynamicNumButtonPager):
    def pre_load(self, webdriver: WebDriver) -> None:
        script = {
            "method": "redirect",
            "url": "https://www.baidu.com/",
            "next": {
                "method": "inputKeyword",
                "xpath": "//*[@id=\"kw\"]",
                "keyword": "和泉雾纱",
                "next": {
                    "method": "click",
                    "xpath": "//*[@id=\"su\"]"
                }
            }
        }
        cl.Script(script)(webdriver)
```

### crawlipt

如果您想要更丰富的脚本，可以使用crawlipt项目

```sh
pip install crawlipt
```

{% embed url="https://github.com/WwwwwyDev/crawlipt" %}
