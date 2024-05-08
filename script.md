---
description: >-
  By using built-in scripts, you can better operate selenium's webdriver. It can
  also facilitate you to store scripts in physical storage such as databases, so
  that you can adjust them faster.
---

# 👾 Script

### Script Definition

The script is a JSON. JSON can be parsed in most languages, making it more versatile. Nesting multiple JSONs to achieve continuous operations.

#### Example

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

Method and its parameters correspond to all [action ](action.md#parms-of-action)method names and their parameters

### Use the script

It is more recommended that you use scripts for [pre\_load](action.md#what-is-pre\_load).

<pre class="language-python"><code class="lang-python"><strong>import crawlist as cl
</strong>
<strong>class MyPager(cl.DynamicNumButtonPager):
</strong>    def pre_load(self, webdriver: WebDriver) -> None:
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
</code></pre>

### crawlipt

If you want a richer script, you can use the crawlipt project

```sh
pip install crawlipt
```

{% embed url="https://github.com/WwwwwyDev/crawlipt" %}
