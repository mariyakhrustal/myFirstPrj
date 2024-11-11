import os
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


def test_log_directory_creation() -> None:
    """Тест на создание директории если её не существует"""

    @log(filename="logs/mylog.txt")
    def division_func(x: Any, y: Any) -> Any:
        return x / y

    division_func(10, 2)

    log_file = "logs/mylog.txt"
    log_dir = os.path.dirname(log_file)

    assert os.path.exists(log_dir)
    assert os.path.exists(log_file)


def test_log_error_in_file() -> None:
    """Тест на успешное выполнение логирования в файл"""

    @log(filename="logs/mylog.txt")
    def division_func(x: Any, y: Any) -> Any:
        return x / y

    log_file = "logs/mylog.txt"
    log_dir = os.path.dirname(log_file)
    if os.path.exists(log_file):
        os.remove(log_file)

    division_func(5, 0)
    assert os.path.exists(log_file)
    with open(log_file, "r", encoding="utf-8") as file:
        log_content = file.read()
    assert log_content == "division_func error: ZeroDivisionError. Inputs: (5, 0), {}\n"
    os.remove(log_file)
    os.rmdir(log_dir)
