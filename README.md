Анализ рейтинга брендов из CSV файлов. Тестовое задание для позиции Python Developer.

## Установка

pip install -r requirements.txt


## Использование

python script.py --files data.csv --report average-rating


### Доступные отчёты:
- `average-rating` - средний рейтинг по брендам


### Как добавить новый отчет:

1. Создать класс в `reports/new_report.py`:

from reports.base import Report

class NewReport(Report):
def generate(self, data: dict[str, list[float]]) -> list[tuple[str, float]]:
# Логика
return result


2. Добавить в реестр `reports/__init__.py`:

from reports.new_report import NewReport

REPORTS_REGISTRY = {
'average-rating': AverageRatingReport,
'new-report': NewReport, 
}


3. Использовать:

python script.py --files data.csv --report new-report
