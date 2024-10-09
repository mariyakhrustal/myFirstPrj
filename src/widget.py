from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_info: str) -> str:
    """Функция обрабатывает информацию о картах и счетах"""
    original_number = card_info.split()[-1]
    if len(original_number) == 16:
        card_number_1 = get_mask_card_number(original_number)
        result = f"{card_info[:-16]}{card_number_1}"
    elif len(original_number) == 20:
        card_number_2 = get_mask_account(original_number)
        result = f"{card_info[:-20]}{card_number_2}"
    return result


def get_date(date_1: str) -> str:
    """Функция возвращает строку с датой в формате 'ДД.ММ.ГГГГ'"""
    date_2, _ = date_1.split("T")
    year, month, day = date_2.split("-")
    return f'"{day}.{month}.{year}"'
