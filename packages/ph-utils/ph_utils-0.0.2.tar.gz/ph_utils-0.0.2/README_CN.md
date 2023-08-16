# ph-utils

`Python3` 工具类.

1. 安装

```shell
pip install ph-utils
```

2. 使用

```python
from ph_utils import date_utils

# date_utils.parse()

from ph_utils.date_utils import parse

# parse()
```

## `date-utils`

日期处理相关的工具类.

### `1. parse(date_data: Any, fmt=None): datetime`

解可以将各种数据格式解析为日期对象，包括时间戳、字符串和日期对象本身。返回值为 `datetime`

1. 解析时间戳

```python
date_utils.parse(1691997308) # 2023-08-14 15:15:08
```

2. 解析字符串

```python
date_utils.parse('2023-08-14 15:23:23') # 2023-08-14 15:23:23
date_utils.parse('20230814 152323') # 2023-08-14 15:23:23
date_utils.parse('2023/08/14 15:23:23', '%Y/%m/%d %H:%M:%S') # 2023-08-14 15:23:23
```

3. 解析 “空” 对象

```python
date_utils.parse() # 2023-08-14 15:15:23.830691
date_utils.parse(None) # 2023-08-14 15:15:23.830691
```

4. 解析日期对象本身

```python
date_utils.parse(date_utils.parse()) # 2023-08-14 15:19:48.382871
```

### `2. format(ori_date, pattern): str`

日期格式化函数，将日期格式化为指定格式的字符串。

参数说明如下：

1. `ori_date`: **可选** 能被 `parse` 函数支持的类型
2. `pattern`: **可选** 默认值：`%Y-%m-%d`，例如：`%Y-%m-%d %H:%M:%S`

```python
date_utils.format(None, '%Y-%m-%d %H:%M:%S')
```

### `3. timestamp(ori_date, unit): int`

获取某个日期的时间戳; `unit` - 定义返回的数据精度, `s` - 精确到秒, `ms` - 精确到毫秒, 默认为：`s`

```python
timestamp()
```

### `4. start_of(ori_date, unit, __format): datetime | int`

设置到一个时间的开始或结束。`__format` 定义返回值类型, `s`、`ms` 返回时间戳；否则返回 `datetime` 对象。`unit` - 设置的时间点, `date` - 当天 `00:00`，默认为：`date`

```python
# 1. 获取当天的开始时间
start_of(unit='date') # start_of()
```

### `5. end_of()`
