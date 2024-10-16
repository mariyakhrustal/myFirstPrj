import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "number, expected",
    [
        ("", "Номер не обнаружен"),
        ("7000792289606361", "7000 79** **** 6361"),
        ("73654108430135874305", "Номер недопустимой длинны"),
        ("70007922", "Номер недопустимой длинны"),
        ("70007n2289606361", "Номер содержит недопустимые символы"),
    ],
)
# Функция маскировки номера банковской карты
def test_get_mask_card_number(number: str, expected: str) -> None:
    assert get_mask_card_number(number) == expected


@pytest.mark.parametrize(
    "account, expected",
    [
        ("", "Номер не обнаружен"),
        ("73654108430135874305", "**4305"),
        ("7000792289606361", "Номер недопустимой длинны"),
        ("73654108430135874305700079", "Номер недопустимой длинны"),
        ("7k6541084n0135874n05", "Номер содержит недопустимые символы"),
    ],
)
# Функция маскировки номера банковского счета
def test_get_mask_account(account: str, expected: str) -> None:
    assert get_mask_account(account) == expected
