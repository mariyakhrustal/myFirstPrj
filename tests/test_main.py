# -*- coding: utf-8 -*-
import pytest
from unittest.mock import patch, MagicMock
from src.main import (
    get_gritting_data,
    get_transacts_source_data,
    get_state_data,
    get_date_data,
    get_currency_data,
    get_filtered_by_word_data,
    get_output_result_data,
    main,
    wrong_output
)


# Тестирование функции приветствия
@patch("builtins.print")
def test_get_gritting_data(mock_print):
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
def test_get_transacts_source_data_csv(mock_get_csv_transacts, mock_input):
    transact_list, user_input = get_transacts_source_data()
    assert user_input == "2"
    assert transact_list == ["mock_data"]
    mock_input.assert_called_once_with("Введите число: ")
    mock_get_csv_transacts.assert_called_once_with("../data/transactions_csv.csv")


@patch("builtins.input", side_effect=["1"])
@patch("src.main.get_operations_data", return_value=["mock_data"])
def test_get_transacts_source_data_json(mock_get_operations_data, mock_input):
    transact_list, user_input = get_transacts_source_data()
    assert user_input == "1"
    assert transact_list == ["mock_data"]
    mock_input.assert_called_once_with("Введите число: ")
    mock_get_operations_data.assert_called_once_with("../data/operations.json")


@patch("builtins.input", side_effect=["3"])
@patch("src.main.get_excel_transacts", return_value=["mock_data"])
def test_get_transacts_source_data_excel(mock_get_excel_transacts, mock_input):
    transact_list, user_input = get_transacts_source_data()
    assert user_input == "3"
    assert transact_list == ["mock_data"]
    mock_input.assert_called_once_with("Введите число: ")
    mock_get_excel_transacts.assert_called_once_with("../data/transactions_excel.xlsx")


# # Тестирование фильтрации по статусу
# @patch("builtins.input", side_effect=["EXECUTED"])
# @patch("src.processing.filter_by_state", return_value=["filtered_by_state"])
# def test_get_state_data(mock_filter_by_state, mock_input):
#     transact_list = ["mock_data"]
#     state_filtered_data = get_state_data(transact_list)
#     assert state_filtered_data == ["filtered_by_state"]
#     mock_input.assert_called_once_with("Введите выбранный статус: ")
#     mock_filter_by_state.assert_called_once_with(transact_list, "EXECUTED")


# # Тестирование фильтрации по дате
# @patch("builtins.input", side_effect=["да", "по убыванию"])
# @patch("src.processing.sort_by_date", return_value=["sorted_data"])
# def test_get_date_data(mock_sort_by_date, mock_input):
#     state_filtered_data = ["mock_data"]
#     sort_filtered_data = get_date_data(state_filtered_data)
#     assert sort_filtered_data == ["sorted_data"]
#     mock_input.assert_any_call("Отфильтровать операции по дате?")
#     mock_input.assert_any_call("Введите: по возрастанию / по убыванию: ")
#     mock_sort_by_date.assert_called_once_with(state_filtered_data, True)


# # Тестирование фильтрации по валюте
# @patch("builtins.input", side_effect=["да", "нет"])
# def test_get_currency_data(mock_input):
#     sort_filtered_data = [{"currency_code": "RUB"}, {"currency_code": "USD"}]
#     rub_filtered_data = get_currency_data(sort_filtered_data, "2")
#     assert len(rub_filtered_data) == 1
#     assert rub_filtered_data[0]["currency_code"] == "RUB"
#     mock_input.assert_any_call("Выводить только рублёвые транзакции?")


# # Тестирование фильтрации по слову в описании
# @patch("builtins.input", side_effect=["да", "example_word"])
# @patch("src.sorting_funcs.search_by_string", return_value=["filtered_by_word"])
# def test_get_filtered_by_word_data(mock_search_by_string, mock_input):
#     rub_filtered_data = ["mock_data"]
#     word_filtered_data = get_filtered_by_word_data(rub_filtered_data)
#     assert word_filtered_data == ["filtered_by_word"]
#     mock_input.assert_called_with("Введите слово для сортировки: ")
#     mock_search_by_string.assert_called_once_with(rub_filtered_data, "example_word")


# # Тестирование вывода данных
# @patch("builtins.print")
# def test_get_output_result_data(mock_print):
#     word_filtered_data = [
#         {"description": "Открытие вклада",
#          "date": "2024-12-01",
#          "operationAmount": {
#              "amount": 1000,
#              "currency":
#                  {"code": "RUB"}
#          }
#          }
#     ]
#     get_output_result_data(word_filtered_data, "1")
#     mock_print.assert_called_with(
#         """2024-12-01 Открытие вклада
#     Сумма: 1000 RUB\n"""
#     )


# Тестирование основного потока программы
@patch("builtins.input", side_effect=["1", "EXECUTED", "да", "по убыванию", "да", "нет"])
@patch("src.main.get_transacts_source_data", return_value=(["mock_data"], "1"))
@patch("src.main.get_state_data", return_value=["state_filtered"])
@patch("src.main.get_date_data", return_value=["date_filtered"])
@patch("src.main.get_currency_data", return_value=["currency_filtered"])
@patch("src.main.get_filtered_by_word_data", return_value=["final_filtered"])
@patch("src.main.get_output_result_data")
def test_main(mock_get_output_result_data, mock_get_filtered_by_word_data, mock_get_currency_data, mock_get_date_data, mock_get_state_data, mock_get_transacts_source_data, mock_input):
    main()
    mock_get_transacts_source_data.assert_called_once()
    mock_get_state_data.assert_called_once_with(["mock_data"])
    mock_get_date_data.assert_called_once_with(["state_filtered"])
    mock_get_currency_data.assert_called_once_with(["date_filtered"], "1")
    mock_get_filtered_by_word_data.assert_called_once_with(["currency_filtered"])
    mock_get_output_result_data.assert_called_once_with(["final_filtered"], "1")
