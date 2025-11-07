"""Модуль для работы с отчётами.

Содержит фабрику для создания отчётов, реестр доступных отчётов
и основной интерфейс для генерирования отчётов разных типов.
"""

from reports.base import Report
from reports.average_rating import AverageRatingReport

REPORTS_REGISTRY = {
    "average-rating": AverageRatingReport,
}


def get_report(report_name: str) -> Report:
    """Получить класс отчёта по названию.

    Args:
        report_name: Название отчёта

    Returns:
        Экземпляр класса отчёта

    Raises:
        ValueError: Если отчёт не найден в реестре
    """
    if report_name not in REPORTS_REGISTRY:
        available = ", ".join(REPORTS_REGISTRY.keys())
        raise ValueError(
            f"Неизвестный отчёт: {report_name}. " f"Доступные: {available}"
        )

    report_class = REPORTS_REGISTRY[report_name]
    return report_class()


def list_available_reports() -> list[str]:
    """Получить список доступных отчётов.

    Returns:
        Список названий доступных отчётов
    """
    return list(REPORTS_REGISTRY.keys())
