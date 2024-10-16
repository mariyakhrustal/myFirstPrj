import pytest


@pytest.fixture
def wrong_length() -> str:
    return "Номер недопустимой длинны"
