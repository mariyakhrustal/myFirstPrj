from typing import Any, Dict, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency_usd(transactions: List[Dict[str, Any]], usd_transactions: Dict[str, Any]) -> None:
    """Тест, что функция корректно фильтрует транзакции по заданной валюте"""
    result = filter_by_currency(transactions, "USD")
    assert next(result) == usd_transactions


def test_filter_by_currency_rub(transactions: List[Dict[str, Any]], rub_transactions: Dict[str, Any]) -> None:
    """Тест, что функция корректно фильтрует транзакции по заданной валюте"""
    result = filter_by_currency(transactions, "RUB")
    assert next(result) == rub_transactions


def test_filter_by_currency_unknown(transactions: List[Dict[str, Any]]) -> None:
    """Тест, что функция правильно обрабатывает случаи, когда транзакции в заданной валюте отсутствуют"""
    with pytest.raises(ValueError, match="Нет транзакций для заданной валюты: T"):
        list(filter_by_currency(transactions, "T"))


def test_filter_by_currency_empty_list() -> None:
    """Тест, что генератор не завершается ошибкой при обработке пустого списка"""
    transactions: list = []
    with pytest.raises(ValueError, match="Список транзакций не может быть пустым"):
        list(filter_by_currency(transactions, "RUB"))


def test_transaction_descriptions_is_correct(transactions: List[Dict[str, Any]]) -> None:
    """Функция тестирует генератор транзакций"""
    num = transaction_descriptions(transactions)
    assert next(num) == "Перевод организации"
    assert next(num) == "Перевод со счета на счет"
    assert next(num) == "Перевод со счета на счет"
    assert next(num) == "Перевод с карты на карту"


def test_transaction_descriptions_empty_list() -> None:
    """Тест на генератор при обработке пустого списка"""
    transactions: list = []
    with pytest.raises(ValueError, match="Список транзакций не может быть пустым"):
        list(transaction_descriptions(transactions))


@pytest.mark.parametrize(
    "start, stop, result",
    [
        (1, 4, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
        (
            12345672,
            12345680,
            [
                "0000 0000 1234 5672",
                "0000 0000 1234 5673",
                "0000 0000 1234 5674",
                "0000 0000 1234 5675",
                "0000 0000 1234 5676",
                "0000 0000 1234 5677",
                "0000 0000 1234 5678",
                "0000 0000 1234 5679",
            ],
        ),
        (1234123412341234, 1234123412341236, ["1234 1234 1234 1234", "1234 1234 1234 1235"]),
        (9999999999999997, 9999999999999999, ["9999 9999 9999 9997", "9999 9999 9999 9998"]),
    ],
)
def test_card_number_generator(start: int, stop: int, result: list) -> None:
    """Тест, что генератор выдает правильные номера карт в заданном диапазоне"""
    generator = list(card_number_generator(start, stop))
    assert generator == result
