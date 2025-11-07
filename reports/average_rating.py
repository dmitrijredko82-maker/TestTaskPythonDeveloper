"""Отчёт среднего рейтинга по брендам."""

from reports.base import Report


class AverageRatingReport(Report):
    """Генерирует отчёт среднего рейтинга по брендам.

    Вычисляет средний рейтинг для каждого бренда,
    валидирует данные и сортирует результаты по убыванию.
    """

    MIN_RATING = 0.0
    MAX_RATING = 5.0

    def generate(self, data: dict[str, list[float]]) -> list[tuple[str, float]]:
        """Генерировать отчёт среднего рейтинга.

        Args:
            data: Словарь {бренд: [рейтинги]}

        Returns:
            Список кортежей (бренд, средний_рейтинг),
            отсортированный по убыванию рейтинга
        """
        # Расчитать средние рейтинги
        averages = self._calculate_averages(data)

        # Отсортировать
        sorted_report = sorted(averages.items(), key=lambda item: (-item[1], item[0]))

        return sorted_report

    def _calculate_averages(self, data: dict[str, list[float]]) -> dict[str, float]:
        """Расчитать средние рейтинги для каждого бренда.

        Args:
            data: Словарь {бренд: [рейтинги]}

        Returns:
            Словарь {бренд: средний_рейтинг}
        """
        averages = {}
        for brand, ratings in data.items():
            if ratings:
                averages[brand] = sum(ratings) / len(ratings)
        return averages

    def is_valid_rating(self, rating: float) -> bool:
        """Проверить что рейтинг в допустимом диапазоне.

        Args:
            rating: Значение рейтинга

        Returns:
            True если рейтинг валиден, False иначе
        """
        return self.MIN_RATING <= rating <= self.MAX_RATING
