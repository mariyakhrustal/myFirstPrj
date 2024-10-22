import pytest

from src.widget import get_date, mask_account_card


# Функция обрабатывает информацию о картах и счетах
@pytest.mark.parametrize(
    "card_info, expected",
    [
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(card_info: str, expected: str) -> None:
    assert mask_account_card(card_info) == expected


def test_mask_account_card_without_empty(no_number: str) -> None:
    assert mask_account_card("") == no_number
    assert mask_account_card("Visa Gold") == no_number
    assert mask_account_card("Maestro") == no_number
    assert mask_account_card("Visa Platinum") == no_number
    assert mask_account_card("MasterCard") == no_number
    assert mask_account_card("Счет") == no_number
    assert mask_account_card("Visa Classic") == no_number


def test_mask_account_card_length(wrong_length: str) -> None:
    assert mask_account_card("Maestro 705199333") == wrong_length
    assert mask_account_card("Счет 6468647364686473678894779589") == wrong_length
    assert mask_account_card("MasterCard 158300734726758") == wrong_length
    assert mask_account_card("Visa Classic 683198111111112476737658") == wrong_length
    assert mask_account_card("Visa Platinum 9") == wrong_length
    assert mask_account_card("Visa Gold 5999414225999414228426353") == wrong_length
    assert mask_account_card("Счет 305") == wrong_length


# Функция возвращает строку с датой в формате 'ДД.ММ.ГГГГ'
@pytest.mark.parametrize(
    "date, expected",
    [
        ("2023-10-18T12:34:56", "18.10.2023"),  # Корректные форматы
        ("2000-01-01T00:00:00", "01.01.2000"),
        ("1999-12-31T23:59:59", "31.12.1999"),
        ("2024-02-29T15:00:00", "29.02.2024"),
        ("2021-07-04T09:30:00", "04.07.2021"),
    ],
)
def test_get_date(date: str, expected: str) -> None:
    assert get_date(date) == expected


def test_get_date_edge_cases() -> None:
    assert get_date("0001-01-01T00:00:00") == "01.01.0001"  # Граничные случаи
    assert get_date("9999-12-31T23:59:59") == "31.12.9999"


def test_get_date_without_separator() -> None:
    with pytest.raises(ValueError, match="Дата должна содержать разделитель 'T'"):
        get_date("2023-10-18 12:34:56")


def test_get_date_empty_date() -> None:
    with pytest.raises(ValueError, match="Дата отсутствует"):
        get_date("T12:34:56")


def test_get_date_invalid_format() -> None:
    with pytest.raises(ValueError, match="Неверный формат даты"):
        get_date("2023-10T12:34:56")


def test_get_date_non_digit_parts() -> None:
    with pytest.raises(ValueError, match="Дата должна содержать только цифры"):
        get_date("2023-10-ABT12:34:56")
