# joyreactor_stats

![PyPI](https://img.shields.io/pypi/v/joyreactor_stats)
![PyPI - License](https://img.shields.io/pypi/l/joyreactor_stats)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/joyreactor_stats)

Получение статистики по публикациям аккаунта на [joyreactor](https://joyreactor.cc)

***

## Установка пакета

### Установка пакета с PyPi

```bash
$ pip install joyreactor-stats
```

### Установка пакета из исходного кода

Исходный код размещается на [GitHub](https://github.com/Genzo4/joyreactor_stats).  
Скачайте его и установите пакет:

```bash
$ git clone https://github.com/Genzo4/joyreactor_stats
$ cd joyreactor_stats
$ pip install .
```

***

## Использование пакета

- ### Подключаем:
```python
from joyreactor_stats import JoyreactorStats
```

- ### Создаём экземпляр
Создаём экземпляр JoyreactorStats.
Нужно указать основной параметр:
- account - аккаунт на Joyrector, для которого собирается статистика. 

Можно указать дополнительные параметры:
- open_xls - открывать в excel полученный отчёт.
  Значение по умолчанию: True
- show_progress - показывать прогресс поиска.
  Значение по умолчанию: True 
- quiet - не выводить никаких сообщений на экран.
  Значение по умолчанию: False

```python
joy_stats = JoyreactorStats('AccountName')
```

- ### Запускаем получение отчёта

```python
joy_stats.work()
```

Пример использования модуля см. в файле main.py

***

# Joyreactor Stats

На основе пакета joyreactor_stats сделана программа Joyreactor Stats.
Готовые билды программы можно взять в релизах на сайте Github (https://github.com/Genzo4/joyreactor_stats/releases)

- ### Билд под Windows
```cmd
pip install -r requirements_build.txt
pyinstaller -F -n joyreactor_stats -i favicon.ico main.py --version-file version.txt
```

Готовый исполняемый файл появляется в папке dist. 

P.S. Для Windows 7 делать билд максимум под Python 3.8

Помощь по параметрам командной строки можно узнать выполнив:
```cmd
joyreactor_stats.exe -h
```

***

[Changelog](https://github.com/Genzo4/joyreactor_stats/blob/main/CHANGELOG.md)
