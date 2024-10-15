from typing import Any


def filter_by_state(bank_transaction_data: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """Возвращает новый список словарей,у которых ключ содержит переданное в функцию значение"""
    list_state = []
    for key in bank_transaction_data:
        if key.get("state") == state:
            list_state.append(key)
    return list_state


def sort_by_date(transaction_data: list[dict[str, Any]], reverse: bool = True) -> list[dict[str, Any]]:
    """Возвращает новый список, в котором исходные словари отсортированы по дате"""
    sorted_info = sorted(transaction_data, key=lambda x: x["date"], reverse=reverse)
    return sorted_info
