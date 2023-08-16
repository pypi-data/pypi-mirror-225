# ph-utils

The python3 tool classes.

1. Install

```shell
pip install ph-utils
```

2. Usage

```python
from ph_utils import date_utils

# date_utils.parse()

from ph_utils.date_utils import parse

# parse()
```

## `date-utils`

The date processing tool.

### `1. parse(date_data: Any, fmt=None): datetime`

You can parse various data formats into date objects, including time stamps, strings, and date objects themselves. Return `datetime` object.

1. parse timestamp

```python
date_utils.parse(1691997308) # 2023-08-14 15:15:08
```

2. parse strings

```python
date_utils.parse('2023-08-14 15:23:23') # 2023-08-14 15:23:23
date_utils.parse('20230814 152323') # 2023-08-14 15:23:23
date_utils.parse('2023/08/14 15:23:23', '%Y/%m/%d %H:%M:%S') # 2023-08-14 15:23:23
```

3. parse `None` object

```python
date_utils.parse() # 2023-08-14 15:15:23.830691
date_utils.parse(None) # 2023-08-14 15:15:23.830691
```

4. parse `datetime`

```python
date_utils.parse(date_utils.parse()) # 2023-08-14 15:19:48.382871
```

### `2. format(ori_date, pattern): str`

Date formatting is the process of converting a date to a specific format.

Parameter description:
1. `ori_date`: **optional** All parameters that can be supported by the `parse` function.
2. `pattern`: **optional** `default: %Y-%m-%d`, eg: `%Y-%m-%d %H:%M:%S`

```python
date_utils.format(None, '%Y-%m-%d %H:%M:%S')
```
