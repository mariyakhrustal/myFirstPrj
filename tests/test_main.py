# -*- coding: utf-8 -*-
from typing import Any
from unittest.mock import MagicMock, patch

from src.main import (get_currency_data, get_date_data, get_filtered_by_word_data, get_gritting_data,
                      get_output_result_data, get_state_data, get_transacts_source_data, main, wrong_output)


# Тестирование функции приветствия
@patch("builtins.print")
def test_get_gritting_data(mock_print: MagicMock) -> None:
    get_gritting_data()
    mock_print.assert_called_once_with(
        """
Привет! Добро пожаловать в программу работы с банковскими транзакциями!
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла;
2. Получить информацию о транзакциях из CSV-файла;
3. Получить информацию о транзакциях из XLSX-файла.
        """
    )


# Тестирование функции выбора источника транзакций
@patch("builtins.input", side_effect=["2"])
@patch("src.main.get_csv_transacts", return_value=["mock_data"])
def test_get_transacts_source_data_csv(mock_get_csv_transacts: MagicMock, mock_input: MagicMock) -> None:
    transact_list, user_input = get_transacts_source_data()
    assert user_input == "2"
    assert transact_list == ["mock_data"]
    mock_input.assert_called_once_with("Введите число: ")
    mock_get_csv_transacts.assert_called_once_with("../data/transactions_csv.csv")


@patch("builtins.input", side_effect=["1"])
@patch("src.main.get_operations_data", return_value=["mock_data"])
def test_get_transacts_source_data_json(mock_get_operations_data: MagicMock, mock_input: MagicMock) -> None:
    transact_list, user_input = get_transacts_source_data()
    assert user_input == "1"
    assert transact_list == ["mock_data"]
    mock_input.assert_called_once_with("Введите число: ")
    mock_get_operations_data.assert_called_once_with("../data/operations.json")


@patch("builtins.input", side_effect=["3"])
@patch("src.main.get_excel_transacts", return_value=["mock_data"])
def test_get_transacts_source_data_excel(mock_get_excel_transacts: MagicMock, mock_input: MagicMock) -> None:
    transact_list, user_input = get_transacts_source_data()
    assert user_input == "3"
    assert transact_list == ["mock_data"]
    mock_input.assert_called_once_with("Введите число: ")
    mock_get_excel_transacts.assert_called_once_with("../data/transactions_excel.xlsx")


@patch("builtins.input", return_value="да")
def test_get_currency_data_with_no_rub(mock_input: MagicMock) -> None:
    sort_filtered_data = [{"currency_code": "RUB"}, {"currency_code": "USD"}]
    user_input = "2"
    result = get_currency_data(sort_filtered_data, user_input)
    assert len(result) == 1
    assert all(transact["currency_code"] == "RUB" for transact in result)


@patch("builtins.input", return_value="нет")
def test_get_currency_data_with_no_filter(mock_input: MagicMock) -> None:
    sort_filtered_data: list[dict[Any, Any]] = [
        {"operationAmount": {"currency": {"code": "RUB"}}},
        {"operationAmount": {"currency": {"code": "USD"}}},
        {"currency_code": "RUB"},
        {"currency_code": "USD"},
    ]
    user_input = "1"
    result = get_currency_data(sort_filtered_data, user_input)
    assert len(result) == 4


# Тест для обработки неверного ввода
@patch("builtins.input", side_effect=["неверно", "да"])
def test_invalid_input_handling(mock_input: MagicMock) -> None:
    sort_filtered_data = [{"operationAmount": {"currency": {"code": "RUB"}}}]
    user_input = "1"
    result = get_currency_data(sort_filtered_data, user_input)
    assert len(result) == 1
    assert all(transact["operationAmount"]["currency"]["code"] == "RUB" for transact in result)


@patch("builtins.input", side_effect=["5", "1"])
@patch("builtins.print")
def test_wrong_output_menu(mock_print: MagicMock, mock_input: MagicMock) -> None:
    _, choice = get_transacts_source_data()
    mock_print.assert_any_call(wrong_output)
    assert choice == "1"


def test_get_state_data_invalid_status() -> None:
    mock_transact_list = [
        {"id": 1, "status": "EXECUTED"},
        {"id": 2, "status": "CANCELED"},
        {"id": 3, "status": "PENDING"},
    ]

    with patch("builtins.input", side_effect=["INVALID", "EXECUTED"]), patch("builtins.print") as mock_print:
        result = get_state_data(mock_transact_list)
        mock_print.assert_any_call(wrong_output)
        assert len(result) == 0


def test_get_date_data_invalid() -> None:
    mock_data = [
        {"id": 1, "date": "2023-10-01", "status": "EXECUTED"},
        {"id": 2, "date": "2024-01-01", "status": "PENDING"},
        {"id": 3, "date": "2022-05-15", "status": "CANCELED"},
    ]
    with (
        patch("builtins.input", side_effect=["123", "456", "да", "по возрастанию"]),
        patch("builtins.print") as mock_print,
    ):
        result = get_date_data(mock_data)
        mock_print.assert_any_call(wrong_output)
        mock_print.assert_any_call("Отфильтровать операции по дате?")
        assert result[0]["date"] == "2022-05-15"
        assert result[1]["date"] == "2023-10-01"
        assert result[2]["date"] == "2024-01-01"


def test_get_date_data_invalid_second() -> None:
    mock_data = [
        {"id": 1, "date": "2023-10-01", "status": "EXECUTED"},
        {"id": 2, "date": "2024-01-01", "status": "PENDING"},
        {"id": 3, "date": "2022-05-15", "status": "CANCELED"},
    ]
    with (
        patch("builtins.input", side_effect=["да", "456", "789", "по возрастанию"]),
        patch("builtins.print") as mock_print,
    ):
        result = get_date_data(mock_data)
        mock_print.assert_any_call(wrong_output)
        mock_print.assert_any_call("Отфильтровать операции по дате?")
        assert result[0]["date"] == "2022-05-15"
        assert result[1]["date"] == "2023-10-01"
        assert result[2]["date"] == "2024-01-01"


def test_get_date_data_filter_ascending() -> None:
    # Мокируем ввод и вывод
    mock_data = [
        {"id": 1, "date": "2023-10-01", "status": "EXECUTED"},
        {"id": 2, "date": "2024-01-01", "status": "PENDING"},
        {"id": 3, "date": "2022-05-15", "status": "CANCELED"},
    ]

    with patch("builtins.input", side_effect=["да", "по возрастанию"]), patch("builtins.print") as mock_print:
        result = get_date_data(mock_data)
        # Проверка, что операции отсортированы по возрастанию
        assert result[0]["date"] == "2022-05-15"
        assert result[1]["date"] == "2023-10-01"
        assert result[2]["date"] == "2024-01-01"
        mock_print.assert_any_call("Отфильтровать операции по дате?")
        mock_print.assert_any_call("Отфильтровать по возрастанию или убыванию?")


def test_get_date_data_filter_descending() -> None:
    # Мокируем ввод и вывод
    mock_data = [
        {"id": 1, "date": "2023-10-01", "status": "EXECUTED"},
        {"id": 2, "date": "2024-01-01", "status": "PENDING"},
        {"id": 3, "date": "2022-05-15", "status": "CANCELED"},
    ]

    with patch("builtins.input", side_effect=["да", "по убыванию"]), patch("builtins.print") as mock_print:
        result = get_date_data(mock_data)
        # Проверка, что операции отсортированы по убыванию
        assert result[0]["date"] == "2024-01-01"
        assert result[1]["date"] == "2023-10-01"
        assert result[2]["date"] == "2022-05-15"
        mock_print.assert_any_call("Отфильтровать операции по дате?")
        mock_print.assert_any_call("Отфильтровать по возрастанию или убыванию?")


def test_get_date_data_no_filter() -> None:
    # Мокируем ввод и вывод
    mock_data = [
        {"id": 1, "date": "2023-10-01", "status": "EXECUTED"},
        {"id": 2, "date": "2024-01-01", "status": "PENDING"},
        {"id": 3, "date": "2022-05-15", "status": "CANCELED"},
    ]

    with patch("builtins.input", side_effect=["нет"]), patch("builtins.print") as mock_print:
        result = get_date_data(mock_data)
        # Проверка, что фильтрация по дате не была применена
        assert result == mock_data
        mock_print.assert_any_call("Отфильтровать операции по дате?")


def test_get_filtered_by_word_data_valid_yes() -> None:
    mock_data = [
        {"id": 1, "description": "Открытие вклада"},
        {"id": 2, "description": "Перевод организации"},
        {"id": 3, "description": "Перевод с карты на карту"},
    ]
    with patch("builtins.input", side_effect=["да", "карт"]), patch("builtins.print") as mock_print:
        result = get_filtered_by_word_data(mock_data)
        assert result[0]["description"] == "Перевод с карты на карту"
        mock_print.assert_any_call("Отфильтровать список по определённому слову в описании?")


def test_get_filtered_by_word_data_valid_no() -> None:
    mock_data = [
        {"id": 1, "description": "Открытие вклада"},
        {"id": 2, "description": "Перевод организации"},
        {"id": 3, "description": "Перевод с карты на карту"},
    ]
    with patch("builtins.input", side_effect=["нет"]), patch("builtins.print") as mock_print:
        result = get_filtered_by_word_data(mock_data)
        assert result == mock_data
        mock_print.assert_any_call("Отфильтровать список по определённому слову в описании?")


def test_get_filtered_by_word_data_invalid() -> None:
    mock_data = [
        {"id": 1, "description": "Открытие вклада"},
        {"id": 2, "description": "Перевод организации"},
        {"id": 3, "description": "Перевод с карты на карту"},
    ]
    with patch("builtins.input", side_effect=["123", "да", "карт"]), patch("builtins.print") as mock_print:
        result = get_filtered_by_word_data(mock_data)
        assert result[0]["description"] == "Перевод с карты на карту"
        mock_print.assert_any_call("Отфильтровать список по определённому слову в описании?")
        mock_print.assert_any_call(wrong_output)


# Тестирование вывода данных
@patch("builtins.print")
def test_get_output_result_data_1(mock_print: MagicMock) -> None:
    word_filtered_data = [
        {
            "description": "Открытие вклада",
            "date": "2024-12-01",
            "operationAmount": {"amount": 1000, "currency": {"code": "RUB"}},
        }
    ]
    get_output_result_data(word_filtered_data, "1")
    mock_print.assert_called_with(
        """01.12.2024 Открытие вклада
    Сумма: 1000 RUB\n"""
    )


@patch("builtins.print")
def test_get_output_result_data_2(mock_print: MagicMock) -> None:
    word_filtered_data = [
        {
            "state": "EXECUTED",
            "date": "2024-12-01T10:50:58.294041",
            "amount": 1000,
            "currency_code": "RUB",
            "description": "Перевод организации",
            "from": "Maestro 1596837868705199",
            "to": "Счет 64686473678894779589",
        },
    ]
    get_output_result_data(word_filtered_data, "2")
    mock_print.assert_called_with(
        """01.12.2024 Перевод организации
    Maestro 1596 83** **** 5199 -> Счет **9589
    Сумма: 1000 RUB\n"""
    )


@patch("builtins.print")
def test_get_output_result_data_empty(mock_print: MagicMock) -> None:
    data: list = []
    get_output_result_data(data, "1")
    mock_print.assert_any_call("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")


# Тестирование основного потока программы
@patch("builtins.input", side_effect=["1", "EXECUTED", "да", "по убыванию", "да", "нет"])
@patch("src.main.get_transacts_source_data", return_value=(["mock_data"], "1"))
@patch("src.main.get_state_data", return_value=["state_filtered"])
@patch("src.main.get_date_data", return_value=["date_filtered"])
@patch("src.main.get_currency_data", return_value=["currency_filtered"])
@patch("src.main.get_filtered_by_word_data", return_value=["final_filtered"])
@patch("src.main.get_output_result_data")
def test_main(
    mock_get_output_result_data: MagicMock,
    mock_get_filtered_by_word_data: MagicMock,
    mock_get_currency_data: MagicMock,
    mock_get_date_data: MagicMock,
    mock_get_state_data: MagicMock,
    mock_get_transacts_source_data: MagicMock,
    mock_input: MagicMock,
) -> None:
    main()
    mock_get_transacts_source_data.assert_called_once()
    mock_get_state_data.assert_called_once_with(["mock_data"])
    mock_get_date_data.assert_called_once_with(["state_filtered"])
    mock_get_currency_data.assert_called_once_with(["date_filtered"], "1")
    mock_get_filtered_by_word_data.assert_called_once_with(["currency_filtered"])
    mock_get_output_result_data.assert_called_once_with(["final_filtered"], "1")
