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
