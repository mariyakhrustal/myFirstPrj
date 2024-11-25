import os
from pathlib import Path
from typing import Any

import pytest

from src.decorators import log


def test_log_console_ok(capsys: pytest.CaptureFixture) -> None:
    """Тестируем успешное выполнение функции с выводом в консоль"""

    @log()
    def add_func(x: Any, y: Any) -> Any:
        return x + y

    add_func(6, 3)
    output = capsys.readouterr()
    assert output.out == "add_func ok\n"


def test_log_console_error(capsys: pytest.CaptureFixture) -> None:
    """Тестируем ошибку при выполнении функции с выводом в консоль"""

    @log()
    def add_func(x: Any, y: Any) -> Any:
        return x + y

    add_func(6, "3")
    output = capsys.readouterr()
    assert output.out == "add_func error: TypeError. Inputs: (6, '3'), {}\n"


def test_log_directory_creation(tmp_path: Path) -> None:
    """Тест на создание директории если её не существует"""
    log_file = tmp_path / "test.logs"

    @log(filename=str(log_file))
    def division_func(x: Any, y: Any) -> Any:
        return x / y

    division_func(10, 2)

    log_dir = os.path.dirname(log_file)

    assert os.path.exists(log_dir)
    assert os.path.exists(log_file)


def test_log_error_in_file(tmp_path: Path) -> None:
    """Тест на успешное выполнение логирования в файл"""
    log_file = tmp_path / "test.logs"

    @log(filename=str(log_file))
    def division_func(x: Any, y: Any) -> Any:
        return x / y

    division_func(5, 0)
    with open(log_file, "r", encoding="utf-8") as file:
        log_content = file.read()
    assert log_content == "division_func error: ZeroDivisionError. Inputs: (5, 0), {}\n"


def test_log_create_directory_if_not_exists(tmp_path: Path) -> None:
    log_file = tmp_path / "logs" / "test.log"

    @log(filename=str(log_file))
    def division_func(x: Any, y: Any) -> Any:
        return x / y

    assert division_func(8, 4) == 2
    assert (tmp_path / "logs").exists()
