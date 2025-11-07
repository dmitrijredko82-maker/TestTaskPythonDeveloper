"""Модуль для загрузки и обработки данных из CSV файлов.

Этот модуль содержит функции для чтения CSV файлов с данными
о товарах и их рейтингах.
"""

import csv
import os
from collections import defaultdict
from typing import Optional

# Константы
DEFAULT_ENCODING = "utf-8"
MAX_RETRIES = 3


def load_products_from_csv(
    filepaths: list[str],
    encoding: str = DEFAULT_ENCODING,
    raise_on_empty: bool = True,  # Добавляем флаг
) -> dict[str, list[dict]]:
    """Загрузить данные из CSV файлов.

    Args:
        filepaths: Список путей к CSV файлам
        encoding: Кодировка файла (по умолчанию utf-8)
        raise_on_empty: Выбросить ошибку если ничего не загружено

    Returns:
        Словарь, где ключ — название бренда, значение — список продуктов

    Raises:
        ValueError: Если не удалось загрузить ни одного файла
        и raise_on_empty=True
    """
    products = defaultdict(list)
    files_loaded = 0

    for filepath in filepaths:
        if not os.path.isfile(filepath):
            print(f"Файл не найден: {filepath}")
            continue

        try:
            with open(filepath, "r", encoding=encoding) as file:
                reader = csv.DictReader(file)

                if reader.fieldnames is None:
                    print(f"Нет заголовков в {filepath}")
                    continue

                for row in reader:
                    try:
                        brand = row["brand"].strip()
                        rating = float(row["rating"])
                        price = float(row["price"])

                        products[brand].append(
                            {
                                "rating": rating,
                                "price": price,
                            }
                        )
                    except (ValueError, KeyError) as error:
                        print(f"Ошибка парсинга в {filepath}: {error}")

                files_loaded += 1

        except FileNotFoundError:
            # Уже проверили выше, но может быть race condition
            print(f"❌ Файл не найден: {filepath}")
        except PermissionError:
            print(f"❌ Нет прав доступа к файлу: {filepath}")
        except UnicodeDecodeError as error:
            print(f"❌ Ошибка кодировки в {filepath}: {error}")
        except csv.Error as error:
            print(f"❌ Ошибка парсинга CSV в {filepath}: {error}")
        except OSError as error:
            # Ловит файловые ошибки (IOError, исключение ОС)
            print(f"❌ Ошибка при чтении {filepath}: {error}")

    if files_loaded == 0 and raise_on_empty:
        raise ValueError("Не удалось загрузить ни один файл")

    return dict(products)


def safe_average(values: list[float]) -> Optional[float]:
    """Расчитать среднее значение.

    Args:
        values: Список значений

    Returns:
        Среднее значение или None если список пуст
    """
    if not values:
        return None

    return sum(values) / len(values)


def sort_by_value(
    data: dict[str, float],
    reverse: bool = True,
) -> list[tuple[str, float]]:
    """Отсортировать словарь по значениям.

    Args:
        data: Словарь для сортировки
        reverse: True для убывания, False для возрастания

    Returns:
        Список кортежей (ключ, значение), отсортированный по значениям
    """
    return sorted(data.items(), key=lambda item: item[1], reverse=reverse)
