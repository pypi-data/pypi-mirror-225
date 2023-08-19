## Date Time Persian

This library helps you to convert the Gregorian date to Iranian date and the Iranian date to Gregorian date.  
You can also get the current time along with the date.

This library is supported by [Sarzemin Danesh](https://lssc.ir) team.

You can contact us by sending an email or following our official page on Instagram:

Email : [info@Lssc.ir](mailto:info@Lssc.ir)

Instagram : [@sarzamin.danesh](https://instagram.com/sarzamin.danesh)

---

## How it works?

Use the following command to install this library

```python
pip install DateTimePersian
```

## Use :

**Display the current date and time.**  
The output is a string.

```python
from DateTimePersian import DateTimePersian
get_date = DateTimePersian()
print(get_date)

_________ output _________
1401/9/5  15:09:48
```

**Only show the current date.**  
The output is a string.

```python
from DateTimePersian import DateTimePersian
get_date = DateTimePersian(TIME=False)
print(get_date)

_________ output _________
1401/9/5
```

**Only show the current time.**  
The output is a string.

```python
from DateTimePersian import DateTimePersian
get_date = DateTimePersian(DATE=False)
print(get_date)

_________ output _________
15:09:48
```

**Command today() :**

The desired function displays the current date in numeric and text formats. Two settings named date and type are defined for it.

Date = “fa” / “en”

Type = int / str

**Ex : Default**

```python
from DateTimePersian import DateTimePersian
get_date = DateTimePersian()
print(get_date.today())

_________ output _________
1401/9/5
```

**Ex : Type = str**

```python
from DateTimePersian import DateTimePersian
get_date = DateTimePersian()
print(get_date.today(Type = str))

_________ output _________
1401 آذر 5
```

**Ex : Date = “en”**

```python
from DateTimePersian import DateTimePersian
get_date = DateTimePersian()
print(get_date.today(Date = "en"))

_________ output _________
2022/11/26
```

**Ex: Date = “en” and Type = str**

```python
from DateTimePersian import DateTimePersian
get_date = DateTimePersian()
print(get_date.today(Date = "en", Type = str))

_________ output _________
2022 Nov 26
```

**Other commands:**

| value | command | type | output |
| --- | --- | --- | --- |
| Year Persian | getYearP() | object | int |
| Year Gregorian | getYearE() | object | int |
| Month Persian | getMonthP() | object | int |
| Month Gregorian | getMonthE() | object | int |
| Day Persian | getDayP() | object | int |
| Day Gregorian | getDayE() | object | int |
| Hour | getHour() | object | str |
| Minutes | getMin() | object | str |
| Seconds | getSec() | object | str |
| leap year | lYear(year) | static | int |
| name day Persian | getNameDayP() | object | str |
| name day Gregorian | getNameDayE(type = 'L' / 'S') | object | str |
| name month Persian | getNameMonthP() | object | str |
| name month Gregorian | getNameMonthE(type = 'en' / 'fa') | object | str |

**Example Leap Year :**

```python
from DateTimePersian import DateTimePersian

print(DateTimePersian.today(1401))

_________ output _________
350
```

**Example name day Persian :**

```python
from DateTimePersian import DateTimePersian
get_date = DateTimePersian()
print(get_date.getNameDayP())

_________ output _________
جمعه
```

**Example name day Gregorian with type = 'L' :**

```python
from DateTimePersian import DateTimePersian
get_date = DateTimePersian()
print(get_date.getNameDayE())

_________ output _________
Friday
```

**Example name day Gregorian with type = 'S' :**

```python
from DateTimePersian import DateTimePersian
get_date = DateTimePersian()
print(get_date.getNameDayE(type = 'S'))

_________ output _________
Fri
```

**Example name month Persian :**

```python
from DateTimePersian import DateTimePersian
get_date = DateTimePersian()
print(get_date.getNameMonthP())

_________ output _________
مرداد
```

**Example name month Gregorian with type = 'en' :**

```python
from DateTimePersian import DateTimePersian
get_date = DateTimePersian()
print(get_date.getNameMonthE())

_________ output _________
Aug
```

**Example name month Gregorian with type = 'fa' :**

```python
from DateTimePersian import DateTimePersian
get_date = DateTimePersian()
print(get_date.getNameMonthE(type = 'fa'))

_________ output _________
اوت
```