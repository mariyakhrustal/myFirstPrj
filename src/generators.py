from typing import Any, Dict, Generator, List

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


def filter_by_currency(transactions_list: List[Dict[str, Any]], currency: str) -> Generator:
    """Функция выдает транзакции по заданной валюте"""
    if any(transactions_list):
        transact = (
            transaction
            for transaction in transactions_list
            if transaction["operationAmount"]["currency"]["code"] == currency
        )
        results = list(transact)
        if not results:
            raise ValueError(f"Нет транзакций для заданной валюты: {currency}")
        for transaction in results:
            yield transaction
    else:
        raise ValueError("Список транзакций не может быть пустым")


# if __name__ == '__main__':
#     usd_transactions = filter_by_currency(transactions, "USD")
#     for _ in range(4):
#         try:
#             print(next(usd_transactions))
#         except StopIteration:
#             print("Нет больше транзакций для заданной валюты")
#             break


def transaction_descriptions(transactions_list: List[Dict[str, Any]]) -> Generator:
    """Функция выдает описание каждой операции"""
    if any(transactions_list):
        descript = (item["description"] for item in transactions_list)
        for description in descript:
            yield description
    else:
        raise ValueError("Список транзакций не может быть пустым")


# if __name__ == '__main__':
#     descriptions = transaction_descriptions(transactions)
#     for _ in range(5):
#         try:
#             print(next(descriptions))
#         except StopIteration:
#             print("Больше нет доступных описаний")
#             break


def card_number_generator(start: int, end: int) -> Generator:
    """
    Функция выдает номера банковских карт в формате
    XXXX XXXX XXXX XXXX, где X — цифра номера карты
    """
    for number in range(start, end):
        card = str(number)
        while len(card) < 16:
            card = "0" + card
        yield f"{card[0:4]} {card[4:8]} {card[8:12]} {card[12:16]}"


# if __name__ == '__main__':
#     for card_number in card_number_generator(1, 5):
#         print(card_number)
