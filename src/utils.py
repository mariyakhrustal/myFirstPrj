import json


def get_operations_data(path: str) -> list:
    """Получение списков транзакций"""
    try:
        with open(path, "r", encoding="utf-8") as operations_file:
            try:
                operations = json.load(operations_file)
                if isinstance(operations, list):
                    return operations
                else:
                    return []
            except json.JSONDecodeError:
                return []
    except FileNotFoundError:
        return []


# if __name__ == '__main__':
#     print(get_operations_data('../data/operations.json'))
