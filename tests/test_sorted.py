from src.sorting_funcs import count_certain_transacts, search_by_string


def test_search_by_string_found(transactions: list[dict]) -> None:
    """Тест на успешный поиск"""
    result = search_by_string(transactions, "счет")
    assert len(result) == 2
    assert result[0]["description"] == "Перевод со счета на счет"
    assert result[1]["description"] == "Перевод со счета на счет"


def test_search_by_string_not_found(transactions: list[dict]) -> None:
    """Тест на не успешный поиск"""
    result = search_by_string(transactions, "111")
    assert result == []


def test_count_certain_transacts_found(transactions: list[dict]) -> None:
    """Тест на подсчет категорий транзакций"""
    list_of_categories = ["перевод с карты", "перевод Организации"]

    result = count_certain_transacts(transactions, list_of_categories)

    assert len(result) == 2
    assert result == {"Перевод организации": 2, "Перевод с карты на карту": 1}


def test_count_certain_transacts_not_found(transactions: list[dict]) -> None:
    """Тест на подсчет несуществующих категорий транзакций"""
    result = count_certain_transacts(transactions, ["123", "456", "789"])
    assert result == {}
