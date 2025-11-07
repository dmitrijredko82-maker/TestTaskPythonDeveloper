"""Главный скрипт для формирования отчётов по рейтингам брендов."""

import argparse
import sys
from tabulate import tabulate

from data.loader import load_products_from_csv
from reports import get_report, list_available_reports


def main() -> int:
    """Главная функция скрипта.
    Returns:
        Код выхода (0 для успеха, 1 для ошибки)
    """
    parser = argparse.ArgumentParser(
        description='Анализ рейтинга брендов',
        epilog='python script.py --files data.csv --report average-rating'
    )

    parser.add_argument(
        '--files',
        nargs='+',
        required=True,
        help='Пути к CSV файлам'
    )

    parser.add_argument(
        '--report',
        required=True,
        choices=list_available_reports(),
        help='Тип отчёта'
    )

    args = parser.parse_args()

    try:
        # 1. Загрузить данные
        all_products = load_products_from_csv(args.files)

        if not all_products:
            raise ValueError("Не удалось загрузить данные")

        # 2. Подготовить данные
        if args.report == 'average-rating':
            data = {
                brand: [product['rating'] for product in products]
                for brand, products in all_products.items()
            }
            headers = ['Brand', 'Average Rating']
        elif args.report == 'average-price':
            data = {
                brand: [product['price'] for product in products]
                for brand, products in all_products.items()
            }
            headers = ['Brand', 'Average Price']
        else:
            raise ValueError(f"Неизвестный отчёт: {args.report}")

        # 3. Получить отчёт
        report = get_report(args.report)

        # 4. Генерировать отчёт
        result = report.generate(data)

        # 5. Форматировать результаты
        formatted_result = [
            (brand, f"{value:.2f}")
            for brand, value in result
        ]

        # 6. Вывести результаты
        report_name = args.report.upper().replace('-', ' ')
        print(f"\n{report_name}\n")
        print(tabulate(formatted_result, headers=headers, tablefmt='grid'))

        return 0

    except FileNotFoundError as error:
        print(f"❌ Файл не найден: {error}")
        return 1
    except UnicodeDecodeError as error:
        print(f"❌ Ошибка кодировки: {error}")
        return 1
    except ValueError as error:
        print(f"❌ Ошибка в данных: {error}")
        return 1
    except KeyError as error:
        print(f"❌ Колонка не найдена: {error}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
