import pytest

from src.masks import get_mask_account, get_mask_card_number


# Функция маскировки номера банковской карты
@pytest.mark.parametrize(
    "number, expected",
    [
        ("700079=289606361", "Номер содержит недопустимые символы"),
        ("700079228 606361", "Номер содержит недопустимые символы"),
        ("7000792289.06361", "Номер содержит недопустимые символы"),
        ("70!0792289606361", "Номер содержит недопустимые символы"),
        ("70007n2289606361", "Номер содержит недопустимые символы"),
        ("70007/2289606361", "Номер содержит недопустимые символы"),
        ("70007_2289606361", "Номер содержит недопустимые символы"),
        ("70007@2289606361", "Номер содержит недопустимые символы"),
        ("70007[2289606361", "Номер содержит недопустимые символы"),
    ],
)
def test_get_mask_card_number_is_digit(number: str, expected: str) -> None:
    assert get_mask_card_number(number) == expected


def test_get_mask_card_number_empty() -> None:
    assert get_mask_card_number("") == "Номер не обнаружен"


def test_get_mask_card_number() -> None:
    assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"


def test_get_mask_card_number_short(wrong_length: str) -> None:
    assert get_mask_card_number("70007922") == wrong_length


def test_get_mask_card_number_long(wrong_length: str) -> None:
    assert get_mask_card_number("73654108430135874305") == wrong_length


# Функция маскировки номера банковского счета
@pytest.mark.parametrize(
    "account, expected",
    [
        ("736541#8430135874305", "Номер содержит недопустимые символы"),
        ("7365410843-135874305", "Номер содержит недопустимые символы"),
        ("7365410843013(874305", "Номер содержит недопустимые символы"),
        ("73654108+30135874305", "Номер содержит недопустимые символы"),
        ("73654108430135{74305", "Номер содержит недопустимые символы"),
        ("736541084301*5874305", "Номер содержит недопустимые символы"),
        ("736541084%0135874305", "Номер содержит недопустимые символы"),
        ("73654:08430135874305", "Номер содержит недопустимые символы"),
        ("7k6541084n0135874n05", "Номер содержит недопустимые символы"),
    ],
)
def test_get_mask_account_is_digit(account: str, expected: str) -> None:
    assert get_mask_account(account) == expected


def test_get_mask_account_empty() -> None:
    assert get_mask_account("") == "Номер не обнаружен"


def test_get_mask_account() -> None:
    assert get_mask_account("73654108430135874305") == "**4305"


def test_get_mask_account_short(wrong_length: str) -> None:
    assert get_mask_account("70007922") == wrong_length


def test_get_mask_account_long(wrong_length: str) -> None:
    assert get_mask_account("73654108430135874305700079") == wrong_length
