# ph-utils

## 安装

```shell
pip install ph-utils
```

The python3 tool classes. Includes the following modules:

1. `config_utils`: Configure relevant tool classes, `load_env`
2. `date_utils`: The date processing tool, `parse`、`format`、`set`、`start_of`、`end_of`、`add`、`sub`、`diff`、`timestamp`

## 1. `config_utils`

Configure relevant tool classes.

### Usage

```python
from ph_utils.config_utils import load_env
```

### `1. load_env(file_dir, env_files): dict`:

Load the environment variable file, the content behind the list will replace the content in front. `file_dir` - The environment variable file folder, default: `os.cwd()`; `env_files` - The environment variable file list, if `None` or empty list load `['.env', '.env.local', '.env.development', '.env.production']`

### `2. load_json(file_dir, json_files): dict`:

Load json file. default: `['config.json']`

### `3. load_ini(file_dir, ini_files): dict`:

Load `ini` file. default: `[config.ini]`

## 2. `date-utils`

The date processing tool.

### Usage

```python
import ph_utils.date_utils as date_utils
from ph_utils.date_utils import parse, format
```

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
date_utils.format(1691997308, '%Y-%m-%d %H:%M:%S')
```

### `3. start_of(ori_date, unit, __format): datetime | int`

Set the start of a time at a certain moment.

Paramater description:

1. `unit`: **optional** `default: date`, `date` - start time of a day
2. `__format`: **optional** `default: None`, set the returned data, `None` - return `datetime`, `s`、`ms` return timestamp

```python
start_of() # datetime - 2023-08-15 00:00:00
start_of(__format='s') # int - 1692028800
```

### `4. end_of(ori_date, unit, __format): datetime | int`

Set the end of a time at a certain moment.

```python
end_of() # datetime - 2023-08-15 23:59:59
```

### `5. timestamp(ori_date, unit): int`

Get timestamp of a time

1. `unit`: `s` - _default_ length: 10，accurate to second、 `ms` length: 13, accurate to milliseconds.

```python
timestamp()
```

### `6. set(ori_date, values): datetime`

Set date values to a given date.

Sets time values to date from object . A value is not set if it is undefined or null or doesn't exist in values.

`values`: `str | dict`，the given date. If is `dict`, include the follow property. `year`、`month`、`day`、`hour`、`minute`、`second`

```python
set(None, '2023-08-15 14:49:49')
set(None, '2023/08/15 14:49:49')
set(None, '20230815 144949')
set(None, '20230815')
set(None, '144949')
set(None, { 'year': 2023, 'month': 8, 'day': 15, 'hour': 14, 'minute': 49, 'second': 49 })
set(None, { 'year': 2023, 'month': 8, 'day': 15 })
set(None, { 'hour': 14, 'minute': 49, 'second': 49 })
```

### `7. add(ori_date, duration): datetime`

Add the specified years, months, weeks, days, hours, minutes and seconds to the given date.

`duration` the object with years, months, weeks, days, hours, minutes and seconds to be added.

```python
add(duration={
  'years': 2,
  'months': 9,
  'days': 7,
  'hours': 5,
  'minutes': 9,
  'seconds': 30,
})
```

### `8. subtract(ori_date, duration): datetime`

Subtract the specified years, months, weeks, days, hours, minutes and seconds from the given date.

```python
subtract(duration={
  'years': 2,
  'months': 9,
  'days': 7,
  'hours': 5,
  'minutes': 9,
  'seconds': 30,
})
```

### `9. sub(ori_date, duration): datetime`

Alias of `subtract`.

### `10: diff(start, end, result): int | timedelta`

Get the number of full day periods between two dates.

`result`: set the returned data. if `result = days` - return `int`, difference in days; otherwise return `timedelta`. default: `days`

```python
diff(parse(), parse()) # => 0
```
