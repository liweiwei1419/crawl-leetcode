```python
import requests

res = requests.get("https://leetcode-cn.com/problemset/all/")
print(res.text)

with open('./a.html','w',encoding='utf-8',) as f:
    f.write(res.text)
```


