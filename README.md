# Brand Rating Analyzer

Анализ рейтинга брендов из CSV файлов. Тестовое задание для позиции Python Developer.

## Особенности

- Чтение данных из CSV файлов (модуль `csv`)
- Расчёт среднего рейтинга по брендам
- Strategy Pattern для расширяемости (легко добавлять новые отчёты)
- Полное покрытие тестами (27 тестов)
- Соответствие PEP 8 и Type Hints
- Красивый вывод таблиц (tabulate)


## Установка

pip install -r requirements.txt


## Использование

python script.py --files data.csv --report average-rating


### Доступные отчёты:
- `average-rating` - средний рейтинг по брендам
