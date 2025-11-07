"""Базовый класс для отчётов.

Определяет абстрактный интерфейс, который должны реализовать все типы отчётов.
"""

from abc import ABC, abstractmethod
from typing import Any


class Report(ABC):  # pylint: disable=too-few-public-methods
    """Абстрактный базовый класс для всех типов отчётов.

    Определяет интерфейс, который должны реализовать все отчёты.

    Примеры подклассов:
        - AverageRatingReport: средний рейтинг по брендам
        - AveragePriceReport: средняя цена по брендам
    """

    @abstractmethod
    def generate(self, data: dict) -> Any:
        """Генерировать отчёт из данных.

        Args:
            data: Исходные данные для отчёта

        Returns:
            Результат отчёта (формат зависит от конкретного отчёта)

        Raises:
            NotImplementedError: Метод должен быть реализован в подклассе
        """
