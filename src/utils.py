import json
import logging
import os

logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)  # pragma: no cover


logger = logging.getLogger("utils")
file_handler = logging.FileHandler(os.path.join(logs_dir, "utils.log"), mode="w")
file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.DEBUG)


def get_operations_data(path: str) -> list:
    """Получение списков транзакций"""
    try:
        logger.info(f"Попытка открыть файл: {path}")
        with open(path, "r", encoding="utf-8") as operations_file:
            try:
                logger.info(f"Загрузка данных из файла: {path}")
                operations = json.load(operations_file)
                if isinstance(operations, list):
                    logger.info(f"Данные успешно загружены: количество транзакций - {len(operations)}")
                    return operations
                else:
                    logger.warning("Загруженные данные не являются списком")
                    return []
            except json.JSONDecodeError as e:
                logger.error(f"Ошибка декодирования JSON {e}")
                return []
    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {e}")
        return []
