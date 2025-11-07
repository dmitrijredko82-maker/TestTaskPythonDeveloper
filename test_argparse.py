"""Тесты для парсинга аргументов командной строки."""

import argparse
import sys
from unittest.mock import patch

import pytest


def test_arguments_parsing():
    """Тест: парсинг аргументов"""
    test_args = [
        "script.py",
        "--files",
        "data1.csv",
        "data2.csv",
        "--report",
        "average-rating",
    ]

    with patch.object(sys, "argv", test_args):
        parser = argparse.ArgumentParser()
        parser.add_argument("--files", nargs="+", required=True)
        parser.add_argument("--report", required=True)

        args = parser.parse_args()

        assert args.files == ["data1.csv", "data2.csv"]
        assert args.report == "average-rating"


def test_missing_required_argument():
    """Тест: отсутствует обязательный аргумент"""
    test_args = ["script.py", "--files", "data.csv"]  # Нет --report

    with patch.object(sys, "argv", test_args):
        parser = argparse.ArgumentParser()
        parser.add_argument("--files", nargs="+", required=True)
        parser.add_argument("--report", required=True)

        with pytest.raises(SystemExit):  # argparse вызывает sys.exit() при ошибке
            parser.parse_args()


def test_multiple_files():
    """Тест: несколько файлов"""
    test_args = [
        "script.py",
        "--files",
        "file1.csv",
        "file2.csv",
        "file3.csv",
        "--report",
        "average-rating",
    ]

    with patch.object(sys, "argv", test_args):
        parser = argparse.ArgumentParser()
        parser.add_argument("--files", nargs="+", required=True)
        parser.add_argument("--report", required=True)

        args = parser.parse_args()

        assert len(args.files) == 3
        assert args.files[0] == "file1.csv"
        assert args.files[2] == "file3.csv"
