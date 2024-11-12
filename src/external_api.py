import requests


url = "https://api.apilayer.com/exchangerates_data/convert"

payload = {
    "amount": "1200",
    "from": "EUR",
    "to": "RUB"
}
headers = {
    "apikey": "yAhY1fYUfWzlksnMuEFTbyLI12iOr9OP"
}

response = requests.get(url, headers=headers, params=payload)


def get_conversion(transaction: dict) -> float:
    """Функция конвертирует валюту и возвращает сумму транзакции"""
    if transaction["operationAmount"]["currency"]["code"] == "RUB":
        return transaction["operationAmount"]["amount"]
    else:
        pass
