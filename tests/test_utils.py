from unittest.mock import MagicMock, patch

from src.utils import get_operations_data


@patch("builtins.open", create=True)
def test_get_operations_data_correct_list(mock_open: MagicMock) -> None:
    """Тест, что функция принимает некорректный формат данных (не список)"""
    mock_file = mock_open.return_value.__enter__.return_value
    mock_file.read.return_value = '[{"login": "testuser", "name": "Test User"}]'
    assert get_operations_data("test.json") == [{"login": "testuser", "name": "Test User"}]
    mock_open.assert_called_once_with("test.json", "r", encoding="utf-8")


@patch("builtins.open", create=True)
def test_get_operations_data_not_list(mock_open: MagicMock) -> None:
    """Тест, что функция принимает некорректный формат данных (не список)"""
    mock_file = mock_open.return_value.__enter__.return_value
    mock_file.read.return_value = '{"login": "testuser", "name": "Test User"}'
    assert get_operations_data("test.json") == []
    mock_open.assert_called_once_with("test.json", "r", encoding="utf-8")


@patch("builtins.open", create=True)
def test_get_operations_data_decode_error(mock_open: MagicMock) -> None:
    """Тест, что функция возвращает пустой список при ошибке декодирования"""
    mock_file = mock_open.return_value.__enter__.return_value
    mock_file.read.return_value = '[{"login": "testuser" "name": "Test User"}]'
    assert get_operations_data("test.json") == []
    mock_open.assert_called_once_with("test.json", "r", encoding="utf-8")


@patch("builtins.open", create=True)
def test_get_operations_data_not_exists_file(mock_open: MagicMock) -> None:
    """Тест, что функция возвращает пустой список, если файл не существует"""
    file_name = "example_file.json"
    mock_open.side_effect = FileNotFoundError
    assert get_operations_data(file_name) == []
    mock_open.assert_called_once_with(file_name, "r", encoding="utf-8")
