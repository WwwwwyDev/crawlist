---
description: >-
  By using built-in scripts, you can better operate selenium's webdriver. It can
  also facilitate you to store scripts in physical storage such as databases, so
  that you can adjust them faster.
---

# 👾 script

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

### Define your own script

<pre class="language-python"><code class="lang-python">class MyAction(cl.Action):
    @staticmethod
    @cl.annotation.check(exclude="driver")
    def myMethod(driver: WebDriver, myparm: str):
        pass
print(MyAction.__dict__)
cl.Script.ACTIONS = MyAction.__dict__
# then the parser can parse your script
<strong>script = {
</strong>    "method": "myMethod",
    "myparm": "",
}
</code></pre>

It is more recommended that you use scripts for [pre\_load](action.md#what-is-pre\_load).
