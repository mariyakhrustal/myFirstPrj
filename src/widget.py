from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_info: str) -> str:
    """Функция обрабатывает информацию о картах и счетах"""
    if len(card_info) > 0:
        original_number = card_info.split()[-1]
        length = len(original_number)
        if original_number.isdigit():
            if length == 16:
                card_number_1 = get_mask_card_number(original_number)
                result = f"{card_info[:-16]}{card_number_1}"
                return result
            elif length == 20:
                card_number_2 = get_mask_account(original_number)
                result = f"{card_info[:-20]}{card_number_2}"
                return result
            return "Номер недопустимой длинны"
        return "Не содержит номер"
    return "Не содержит номер"


def get_date(original_date: str) -> str:
    """Функция возвращает строку с датой в формате 'ДД.ММ.ГГГГ'"""
    return datetime.fromisoformat(original_date).strftime("%d.%m.%Y")
