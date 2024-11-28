# -*- coding: utf-8 -*-
import re
from collections import Counter


def search_by_string(operations: list[dict], search_string: str) -> list[dict]:
    """Функция для поиска транзакций, у которых в описании есть указанная строка"""
    pattern = rf"{search_string}"
    searched = [
        transact for transact in operations if re.findall(pattern, transact["description"], flags=re.IGNORECASE)
    ]
    return searched


def count_certain_transacts(operations: list[dict], categories: list[str]) -> dict:
    """Функция для подсчета количества банковских операций определенного типа"""
    category_list = []
    for transact in operations:
        for category in categories:
            pattern = rf"{category}"
            if re.findall(pattern, transact["description"], flags=re.IGNORECASE):
                category_list.append(transact["description"])
    counted = Counter(category_list)
    return dict(counted)


transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    },
    {
        "id": 895315941,
        "state": "EXECUTED",
        "date": "2018-08-19T04:27:37.904916",
        "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод с карты на карту",
        "from": "Visa Classic 6831982476737658",
        "to": "Visa Platinum 8990922113665229",
    },
    {
        "id": 594226727,
        "state": "CANCELED",
        "date": "2018-09-12T21:27:25.241689",
        "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод организации",
        "from": "Visa Platinum 1246377376343588",
        "to": "Счет 14211924144426031657",
    },
]


# if __name__ == '__main__':
#     print(search_by_string(transactions, "организации"))
#     print(count_certain_transacts(transactions, ["перевод с карты", "перевод Организации"]))
