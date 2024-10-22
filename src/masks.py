def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты"""
    length = len(card_number)
    if length < 1:
        return "Номер не обнаружен"
    if length > 16 or length < 16:
        return "Номер недопустимой длинны"
    if not card_number.isdigit():
        return "Номер содержит недопустимые символы"
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Функция маскировки номера банковского счета"""
    length = len(account_number)
    if length < 1:
        return "Номер не обнаружен"
    if length > 20 or length < 20:
        return "Номер недопустимой длинны"
    if not account_number.isdigit():
        return "Номер содержит недопустимые символы"
    return f"**{account_number[-4:]}"
