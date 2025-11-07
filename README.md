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

### Примеры роботы кода:

1. С исходными данными из задания
<img width="887" height="220" alt="{B58F57D4-2FAA-4CBD-91AC-97774A4B01A6}" src="https://github.com/user-attachments/assets/9dd5787b-2a87-4584-99a0-ca2aa4ace8c9" />

2. С новыми данными (products3.csv)
<img width="980" height="225" alt="{7CC27178-2CF5-4917-BCDD-590D387F693D}" src="https://github.com/user-attachments/assets/9029e561-0568-4c86-9d0a-d6bb7573cba6" />
