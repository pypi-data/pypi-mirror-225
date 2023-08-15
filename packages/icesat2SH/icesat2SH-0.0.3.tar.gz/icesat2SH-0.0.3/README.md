# icesat2SH

This Python package is for downloading icesat2 points


# Installation

To install from package manager:

```
pip install icesat2SH
```


# Usage
All entries must be strings

photonConfidence = 'all' or 'noise' or 'buffer' or 'low' or 'medium' or 'high'

Date input format: 'yyyy-mm-dd'		example = '2019-02-08'

```python
import requests
import json
from datetime import datetime, timedelta


ATL03(photonConfidence,Start_date,End_date,miny,minx,maxy,maxx)
#example = ATL03('medium', '2019-05-12', '2019-05-20',52.43,29.54,52.56,29.67)
```

```
output : Two files are created in txt format

```


# License
[MIT licence](./LICENSE)
