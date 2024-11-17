# import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")
headers = {"apikey": api_key}


def get_conversion(transaction: dict) -> float:
    """Функция конвертирует валюту и возвращает сумму транзакции в рублях."""
    try:
        if (
            "operationAmount" in transaction
            and "amount" in transaction["operationAmount"]
            and "currency" in transaction["operationAmount"]
        ):
            amount_value = float(transaction["operationAmount"]["amount"])
            currency_code = transaction["operationAmount"]["currency"]["code"]
            if currency_code == "RUB":
                return amount_value
            elif currency_code != "RUB":
                url = "https://api.apilayer.com/exchangerates_data/convert"
                params = {"from": currency_code, "to": "RUB", "amount": amount_value}
                response = requests.get(url, headers=headers, params=params)
                if response.status_code == 200:
                    data = response.json()
                    if "result" in data:
                        return round(float(data["result"]), 2)
                else:
                    print(f"Ошибка API: {response.status_code}")
        return 0.0
    except Exception as e:
        print(f"Ошибка при конвертации: {e}")
        return 0.0


# with open("data/operations.json", "r", encoding="utf-8") as file:
#     operations = json.load(file)
#
# for i in operations:
#     print(get_conversion(i))
