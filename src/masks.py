import logging
import os

logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)  # pragma: no cover


logger = logging.getLogger("masks")
file_handler = logging.FileHandler(os.path.join(logs_dir, "masks.log"), mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_mask_card_number(card_number: str) -> str:
    """Функция маскировки номера банковской карты"""
    try:
        logger.info(f"Получен номер карты {card_number}")
        length = len(card_number)
        if not length:
            logger.error("Номер карты не обнаружен")
            return "Номер не обнаружен"
        if length != 16:
            logger.error(f"Номер карты имеет недопустимую длинну {length}")
            return "Номер недопустимой длинны"
        if not card_number.isdigit():
            logger.error("Номер карты содержит недопустимые символы")
            return "Номер содержит недопустимые символы"
        masked_card_number = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        logger.info("Номер карты успешно замаскирован")
        return masked_card_number
    except Exception as e:  # pragma: no cover
        logger.error(f"Произошла ошибка {e}")
        return "Ошибка"


def get_mask_account(account_number: str) -> str:
    """Функция маскировки номера банковского счета"""
    try:
        logger.info(f"Получен номер счета {account_number}")
        length = len(account_number)
        if not length:
            logger.error("Номер счета не обнаружен")
            return "Номер не обнаружен"
        if length != 20:
            logger.error(f"Номер счета имеет недопустимую длинну {length}")
            return "Номер недопустимой длинны"
        if not account_number.isdigit():
            logger.error("Номер карты содержит недопустимые символы")
            return "Номер содержит недопустимые символы"
        masked_account_number = f"**{account_number[-4:]}"
        logger.info("Номер счета успешно замаскирован")
        return masked_account_number
    except Exception as e:  # pragma: no cover
        logger.error(f"Произошла ошибка {e}")
        return "Ошибка"
