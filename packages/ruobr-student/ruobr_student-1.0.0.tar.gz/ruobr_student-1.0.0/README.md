<img src="https://i.imgur.com/oOevaNh.gif"/>

Модуль для парсинга Cabinet.ruobr.ru  на ***Python 3.10 и выше***.

## Установка
**GitHub**
```
pip install git+https://github.com/QuoNaro/ruobr-student.git
```
**PyPi**
```
pip install ruobr-student
```

## Использование
```python
from ruobr_student import RuobrCookies, RuobrParser

cookie = RuobrCookies('login','password')
Ruobr = RuobrParser(cookie)
```
## Примечание
> Парсер используется только для **https://cabinet.ruobr.ru/student/**

## Полезные ссылки
- [API для Cabinet Ruobr для школьников и их родителей](https://github.com/raitonoberu/ruobr_api)



