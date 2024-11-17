import os
from unittest.mock import MagicMock, patch

from dotenv import load_dotenv

from src.external_api import get_conversion

load_dotenv()

url = "https://api.apilayer.com/exchangerates_data/convert"
api_key = os.getenv("API_KEY")
headers = {"apikey": api_key}
params = {"from": "USD", "to": "RUB", "amount": 1000.0}


def test_get_conversion_rub() -> None:
    """Тест с валидной транзакцией в рублях"""
    transaction = {"operationAmount": {"amount": "1000.0", "currency": {"code": "RUB"}}}
    assert get_conversion(transaction) == 1000.0


@patch("requests.get")
def test_get_conversion_not_rub(mock_get: MagicMock) -> None:
    """Тест с валидной транзакцией в валюте не рубль"""
    transaction = {"operationAmount": {"amount": "1000.0", "currency": {"code": "USD"}}}
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"result": 60.0}
    assert get_conversion(transaction) == 60.0
    mock_get.assert_called_once_with(url, headers=headers, params=params)


@patch("requests.get")
def test_get_conversion_api_error(mock_get: MagicMock) -> None:
    """Тест с ошибкой в API-запросе (например, неверный ответ от сервера)"""
    transaction = {"operationAmount": {"amount": "1000.0", "currency": {"code": "USD"}}}
    mock_get.return_value.status_code = 500
    assert get_conversion(transaction) == 0.0
    mock_get.assert_called_once_with(url, headers=headers, params=params)


@patch("requests.get")
def test_get_conversion(mock_get: MagicMock) -> None:
    """Тест на исключение"""
    transaction = {"operationAmount": {"amount": "1000.0", "currency": {"code": "USD"}}}
    mock_get.side_effect = Exception("test exception")
    assert get_conversion(transaction) == 0.0
    mock_get.assert_called_once_with(url, headers=headers, params=params)
