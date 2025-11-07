"""Тесты для отчётов."""

# pylint: disable=redefined-outer-name

import pytest

from reports.average_rating import AverageRatingReport


@pytest.fixture
def sample_ratings():
    """Fixture: тестовые рейтинги."""
    return {"apple": [4.9, 4.8], "samsung": [4.8, 4.7, 4.6], "xiaomi": [4.6]}


@pytest.fixture
def sample_prices():
    """Fixture: тестовые цены."""
    return {"apple": [999, 1099], "samsung": [1199, 1299], "xiaomi": [199]}


# ====== Тесты для AverageRatingReport ======


def test_average_rating_calculation(sample_ratings):
    """Тест: расчёт среднего рейтинга."""
    report = AverageRatingReport()
    result = report.generate(sample_ratings)

    # Результат должен быть отсортирован по убыванию
    assert result[0][0] == "apple"  # apple первая
    assert result[0][1] == 4.85  # средний рейтинг 4.85
    assert result[1][0] == "samsung"  # samsung вторая
    assert abs(result[1][1] - 4.7) < 0.01  # средний рейтинг ~4.7
    assert result[2][0] == "xiaomi"  # xiaomi последняя


def test_average_rating_sorting(sample_ratings):
    """Тест: сортировка по убыванию рейтинга."""
    report = AverageRatingReport()
    result = report.generate(sample_ratings)

    # Рейтинги должны быть в убывающем порядке
    assert result[0][1] >= result[1][1]
    assert result[1][1] >= result[2][1]


def test_average_rating_validation():
    """Тест: валидация рейтинга."""
    report = AverageRatingReport()

    assert report.is_valid_rating(4.5) is True
    assert report.is_valid_rating(0.0) is True
    assert report.is_valid_rating(5.0) is True
    assert report.is_valid_rating(-1.0) is False
    assert report.is_valid_rating(6.0) is False


# ====== Тесты граничных случаев ======


def test_empty_ratings():
    """Тест: пустые рейтинги."""
    report = AverageRatingReport()
    result = report.generate({})

    assert result == []


def test_single_brand():
    """Тест: один бренд."""
    report = AverageRatingReport()
    data = {"apple": [4.9, 4.8]}
    result = report.generate(data)

    assert len(result) == 1
    assert result[0][0] == "apple"
    assert result[0][1] == 4.85


def test_single_rating():
    """Тест: один рейтинг для бренда."""
    report = AverageRatingReport()
    data = {"apple": [4.5]}
    result = report.generate(data)

    assert len(result) == 1
    assert result[0][1] == 4.5


def test_equal_ratings():
    """Тест: одинаковые рейтинги."""
    report = AverageRatingReport()
    data = {"apple": [4.5, 4.5], "samsung": [4.5, 4.5], "xiaomi": [4.5, 4.5]}
    result = report.generate(data)

    # Все рейтинги равны 4.5
    assert all(rating == 4.5 for _, rating in result)
    # Должны быть отсортированы по имени (вторичная сортировка)
    assert result[0][0] == "apple"
    assert result[1][0] == "samsung"
    assert result[2][0] == "xiaomi"


def test_high_and_low_ratings():
    """Тест: высокие и низкие рейтинги."""
    report = AverageRatingReport()
    data = {"premium": [5.0, 5.0], "budget": [1.0, 1.0]}
    result = report.generate(data)

    assert result[0][0] == "premium"
    assert result[0][1] == 5.0
    assert result[1][0] == "budget"
    assert result[1][1] == 1.0
