from typing import Any

import pytest

from src.processing import filter_by_state, sort_by_date


# Функция возвращает новый список словарей,у которых ключ содержит переданное в функцию значение
def test_filter_by_state_executed(transactions_list: list[dict[str, Any]]) -> None:
    expected = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]
    assert filter_by_state(transactions_list) == expected


def test_filter_by_state_canceled(transactions_list: list[dict[str, Any]]) -> None:
    expected = [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    assert filter_by_state(transactions_list, state="CANCELED") == expected


def test_filter_by_state_empty() -> None:
    transactions: list = []
    assert filter_by_state(transactions) == []


def test_filter_by_state_no_matches() -> None:
    transactions = [
        {"id": 41428829, "state": "PENDING", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "PENDING", "date": "2018-06-30T02:08:58.425572"},
    ]
    assert filter_by_state(transactions) == []


# Функция возвращает новый список, в котором исходные словари отсортированы по дате
@pytest.mark.parametrize(
    "reverse, expected",
    [
        (
            True,
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},  # Проверка
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},  # сортировки
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},  # по дате
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        (
            False,
            [
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            ],
        ),
    ],
)
def test_sort_by_date(reverse: bool, expected: list[dict[str, Any]]) -> None:
    transactions = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    assert sort_by_date(transactions, reverse) == expected


def test_sort_by_date_empty() -> None:
    transactions: list = []
    assert sort_by_date(transactions) == []


@pytest.mark.parametrize(
    "reverse, expected",
    [
        (
            True,
            [
                {"id": 939719570, "state": "EXECUTED", "date": "2018-09-12T21:27:25.241689"},  # Сортировка по индексу,
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},  # если даты одинаковые
            ],
        ),
        (
            False,
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-09-12T21:27:25.241689"},
            ],
        ),
    ],
)
def test_sort_by_the_same_date(reverse: bool, expected: list[dict[str, Any]]) -> None:
    transactions = [
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-09-12T21:27:25.241689"},
    ]
    assert sort_by_date(transactions, reverse) == expected
