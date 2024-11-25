from typing import Any
from unittest.mock import MagicMock

from src.csv_excel_reader import get_csv_transacts, get_excel_transacts


def test_get_csv_transacts(mock_read_csv: MagicMock, mock_data_csv_excel: list[dict[str, Any]]) -> None:
    """Test get csv data"""
    result = get_csv_transacts("mock_path.csv")
    assert result == mock_data_csv_excel
    mock_read_csv.assert_called_once_with("mock_path.csv")


def test_get_csv_transacts_wrong_path() -> None:
    """Test get empty list from wrong path csv"""
    assert get_csv_transacts(" ") == []
    assert get_csv_transacts("1234") == []
    assert get_excel_transacts("example.csv") == []


def test_get_excel_transacts(mock_read_excel: MagicMock, mock_data_csv_excel: list[dict[str, Any]]) -> None:
    """Test get excel data"""
    result = get_excel_transacts("mock_path.xlsx")
    assert result == mock_data_csv_excel
    mock_read_excel.assert_called_once_with("mock_path.xlsx")


def test_get_excel_transacts_wrong_path() -> None:
    """Test get empty list from wrong path csv"""
    assert get_excel_transacts(" ") == []
    assert get_excel_transacts("1234") == []
    assert get_excel_transacts("example.xlsx") == []
