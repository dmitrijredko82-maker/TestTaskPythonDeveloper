"""Тесты для загрузки данных из CSV файлов."""

# pylint: disable=redefined-outer-name
# pylint: disable=duplicate-code

import csv
import os
import tempfile
from collections import defaultdict

import pytest

def _process_row(row: dict, filepath: str, row_num: int) -> dict | None:
    """Обработать одну строку CSV.

    Args:
        row: Словарь с данными строки
        filepath: Путь к файлу (для сообщений об ошибках)
        row_num: Номер строки (для сообщений об ошибках)

    Returns:
        Словарь с данными продукта или None если ошибка
    """
    try:
        brand = row["brand"].strip()
        rating = float(row["rating"])
        price = float(row["price"])

        return {
            "brand": brand,
            "rating": rating,
            "price": price,
        }
    except KeyError as error:
        print(f"⚠️  {filepath}:{row_num} - колонка не найдена: {error}")
    except ValueError as error:
        print(f"⚠️  {filepath}:{row_num} - ошибка преобразования типа: {error}")

    return None


def _process_file(filepath: str, products: defaultdict, encoding: str) -> int:
    """Обработать один CSV файл.

    Args:
        filepath: Путь к файлу
        products: Словарь для сохранения данных (изменяется на месте)
        encoding: Кодировка файла

    Returns:
        Количество успешно загруженных строк
    """
    if not os.path.isfile(filepath):
        print(f"⚠️  Файл не найден: {filepath}")
        return 0

    if not _has_valid_headers(filepath, encoding):
        return 0

    return _load_rows(filepath, products, encoding)


def _has_valid_headers(filepath: str, encoding: str) -> bool:
    """Проверить что файл имеет валидные заголовки.

    Args:
        filepath: Путь к файлу
        encoding: Кодировка файла

    Returns:
        True если заголовки валидны, False иначе
    """
    try:
        with open(filepath, "r", encoding=encoding) as file:
            reader = csv.DictReader(file)
            if reader.fieldnames is None:
                print(f"⚠️  Нет заголовков в {filepath}")
                return False
            return True
    except PermissionError:
        print(f"❌ Нет прав доступа к файлу: {filepath}")
    except UnicodeDecodeError as error:
        print(f"❌ Ошибка кодировки в {filepath}: {error}")
    except csv.Error as error:
        print(f"❌ Ошибка парсинга CSV в {filepath}: {error}")
    except OSError as error:
        print(f"❌ Ошибка при чтении {filepath}: {error}")

    return False


def _load_rows(filepath: str, products: defaultdict, encoding: str) -> int:
    """Загрузить строки из файла.

    Args:
        filepath: Путь к файлу
        products: Словарь для сохранения данных (изменяется на месте)
        encoding: Кодировка файла

    Returns:
        Количество успешно загруженных строк
    """
    rows_loaded = 0

    try:
        with open(filepath, "r", encoding=encoding) as file:
            reader = csv.DictReader(file)

            for row_num, row in enumerate(reader, start=2):
                product = _process_row(row, filepath, row_num)
                if product:
                    brand = product["brand"]
                    products[brand].append(
                        {
                            "rating": product["rating"],
                            "price": product["price"],
                        }
                    )
                    rows_loaded += 1

    except (PermissionError, UnicodeDecodeError, csv.Error, OSError) as error:
        print(f"❌ Ошибка при обработке {filepath}: {error}")

    return rows_loaded


def load_products_from_csv(
    filepaths: list[str],
    encoding: str = 'utf-8',
    raise_on_empty: bool = True,
) -> dict[str, list[dict]]:
    """Загрузить данные из CSV файлов.

    Читает CSV файлы и агрегирует данные по брендам.

    Args:
        filepaths: Список путей к CSV файлам
        encoding: Кодировка файла (по умолчанию utf-8)
        raise_on_empty: Выбросить ошибку если ничего не загружено (по умолчанию True)

    Returns:
        Словарь, где ключ — название бренда, значение — список продуктов

    Raises:
        ValueError: Если не удалось загрузить ни одного файла и raise_on_empty=True

    Example:
        >>> data = load_products_from_csv(['data.csv'])
        >>> print(data['apple'])
        [{'rating': 4.9, 'price': 999}]
    """
    products: defaultdict[str, list] = defaultdict(list)
    total_rows = 0

    for filepath in filepaths:
        rows = _process_file(filepath, products, encoding)
        total_rows += rows

    result = dict(products)

    if not result and raise_on_empty:
        raise ValueError("Не удалось загрузить ни один файл")

    if total_rows > 0:
        print(f"✅ Успешно загружено {total_rows} строк")

    return result


@pytest.fixture
def sample_csv_file_with_data():
    """Fixture: временный CSV файл с данными."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, newline=""
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["name", "brand", "price", "rating"])
        writer.writerow(["iPhone 15 Pro", "apple", "999", "4.9"])
        writer.writerow(["Galaxy S23", "samsung", "1199", "4.8"])
        writer.writerow(["Redmi Note 12", "xiaomi", "199", "4.6"])
        temp_path = f.name

    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def empty_csv_file():
    """Fixture: временный CSV файл только с заголовками."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, newline=""
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["name", "brand", "price", "rating"])
        temp_path = f.name

    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def invalid_rating_csv_file():
    """Fixture: CSV файл с неправильным рейтингом."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, newline=""
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["name", "brand", "price", "rating"])
        writer.writerow(["iPhone", "apple", "999", "invalid"])
        temp_path = f.name

    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def single_brand_csv_file():
    """Fixture: CSV файл с одним брендом."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, newline=""
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["name", "brand", "price", "rating"])
        writer.writerow(["Phone 0", "apple", "900", "4.9"])
        temp_path = f.name

    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def two_brands_csv_files():
    """Fixture: два CSV файла с разными брендами."""
    files = []

    # Первый файл - apple
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, newline=""
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["name", "brand", "price", "rating"])
        writer.writerow(["Phone 0", "apple", "900", "4.9"])
        files.append(f.name)

    # Второй файл - samsung
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, newline=""
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["name", "brand", "price", "rating"])
        writer.writerow(["Phone 1", "samsung", "1000", "4.8"])
        files.append(f.name)

    yield files

    for filepath in files:
        os.unlink(filepath)


@pytest.fixture
def multiple_ratings_csv_file():
    """Fixture: CSV файл с несколькими рейтингами для одного бренда."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, newline=""
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["name", "brand", "price", "rating"])
        writer.writerow(["iPhone 15", "apple", "999", "4.9"])
        writer.writerow(["iPhone 14", "apple", "899", "4.8"])
        writer.writerow(["iPhone 13", "apple", "799", "4.7"])
        temp_path = f.name

    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def missing_column_csv_file():
    """Fixture: CSV файл с отсутствующей колонкой."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, newline=""
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["name", "price", "rating"])  # Нет 'brand'!
        writer.writerow(["iPhone", "999", "4.9"])
        temp_path = f.name

    yield temp_path
    os.unlink(temp_path)


@pytest.fixture
def case_sensitive_csv_file():
    """Fixture: CSV файл для проверки case-sensitivity."""
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False, newline=""
    ) as f:
        writer = csv.writer(f)
        writer.writerow(["name", "brand", "price", "rating"])
        writer.writerow(["Phone 1", "Apple", "999", "4.9"])
        writer.writerow(["Phone 2", "apple", "899", "4.8"])
        temp_path = f.name

    yield temp_path
    os.unlink(temp_path)


# ====== Основные тесты ======


def test_load_single_file(sample_csv_file_with_data):
    """Тест: загрузить один файл."""
    result = load_products_from_csv([sample_csv_file_with_data])

    assert "apple" in result
    assert "samsung" in result
    assert "xiaomi" in result
    assert len(result["apple"]) == 1
    assert result["apple"][0]["rating"] == 4.9
    assert result["apple"][0]["price"] == 999


# ====== Тесты для обработки отсутствующих файлов ======


def test_file_not_found_returns_empty():
    """Тест: пустой словарь если файл не найден и raise_on_empty=False."""
    result = load_products_from_csv(["nonexistent.csv"], raise_on_empty=False)

    assert not result


def test_file_not_found_raises():
    """Тест: исключение если файл не найден и raise_on_empty=True."""
    with pytest.raises(ValueError, match="Не удалось загрузить ни один файл"):
        load_products_from_csv(["nonexistent.csv"], raise_on_empty=True)


def test_file_not_found_default_raises():
    """Тест: по умолчанию выбрасывает исключение."""
    with pytest.raises(ValueError, match="Не удалось загрузить ни один файл"):
        load_products_from_csv(["nonexistent.csv"])


# ====== Другие тесты ======


def test_multiple_files_one_missing(single_brand_csv_file):
    """Тест: один файл есть, другой нет."""
    result = load_products_from_csv([single_brand_csv_file, "nonexistent.csv"])

    assert "apple" in result
    assert len(result["apple"]) == 1


def test_empty_file(empty_csv_file):
    """Тест: пустой файл (только заголовки)."""
    with pytest.raises(ValueError, match="Не удалось загрузить ни один файл"):
        load_products_from_csv([empty_csv_file])


def test_empty_file_no_raise(empty_csv_file):
    """Тест: пустой файл не выбрасывает ошибку если raise_on_empty=False."""
    result = load_products_from_csv([empty_csv_file], raise_on_empty=False)

    assert not result


def test_invalid_rating(invalid_rating_csv_file):
    """Тест: неправильный рейтинг (не число)."""
    with pytest.raises(ValueError, match="Не удалось загрузить ни один файл"):
        load_products_from_csv([invalid_rating_csv_file])


def test_invalid_rating_no_raise(invalid_rating_csv_file):
    """Тест: неправильный рейтинг не выбрасывает ошибку если raise_on_empty=False."""
    result = load_products_from_csv([invalid_rating_csv_file], raise_on_empty=False)

    assert not result


def test_multiple_files(two_brands_csv_files):
    """Тест: загрузить несколько файлов."""
    result = load_products_from_csv(two_brands_csv_files)

    assert "apple" in result
    assert "samsung" in result
    assert len(result["apple"]) == 1
    assert len(result["samsung"]) == 1


def test_data_aggregation(sample_csv_file_with_data):
    """Тест: данные из одного файла агрегируются правильно."""
    result = load_products_from_csv([sample_csv_file_with_data])

    # Проверить что все бренды загружены
    assert len(result) == 3

    # Проверить структуру данных
    assert isinstance(result["apple"], list)
    assert isinstance(result["apple"][0], dict)
    assert "rating" in result["apple"][0]
    assert "price" in result["apple"][0]


def test_data_types(sample_csv_file_with_data):
    """Тест: типы данных конвертированы правильно."""
    result = load_products_from_csv([sample_csv_file_with_data])

    # Проверить что rating это float
    assert isinstance(result["apple"][0]["rating"], float)
    # Проверить что price это float
    assert isinstance(result["apple"][0]["price"], float)


def test_multiple_ratings_per_brand(multiple_ratings_csv_file):
    """Тест: несколько рейтингов для одного бренда."""
    result = load_products_from_csv([multiple_ratings_csv_file])

    # Три рейтинга для apple
    assert len(result["apple"]) == 3
    assert result["apple"][0]["rating"] == 4.9
    assert result["apple"][1]["rating"] == 4.8
    assert result["apple"][2]["rating"] == 4.7


def test_missing_required_column(missing_column_csv_file):
    """Тест: отсутствует необходимая колонка."""
    with pytest.raises(ValueError, match="Не удалось загрузить ни один файл"):
        load_products_from_csv([missing_column_csv_file])


def test_missing_required_column_no_raise(missing_column_csv_file):
    """Тест: отсутствующая колонка не выбрасывает ошибку если raise_on_empty=False."""
    result = load_products_from_csv([missing_column_csv_file], raise_on_empty=False)

    assert not result


def test_case_sensitivity(case_sensitive_csv_file):
    """Тест: разные бренды (case-sensitive)."""
    result = load_products_from_csv([case_sensitive_csv_file])

    # Apple и apple — разные ключи (case-sensitive)
    assert "Apple" in result
    assert "apple" in result
    assert len(result["Apple"]) == 1
    assert len(result["apple"]) == 1
