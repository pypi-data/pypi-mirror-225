`PYTHON URL SHORTNER © 2023`

```bash
pip install shortners
```


```python

import asyncio
from Shortners import Slink

ORGINAL_LINK = ""
SHORTNER_URL = ""
SHORTNER_API = ""

async def test():
    o = await Slink(SHORTNER_URL, SHORTNER_API, ORGINAL_LINK)
    print(f"YOUR SHORTED LINK : {o}")

asyncio.run(test())

```


