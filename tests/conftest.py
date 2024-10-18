import pytest


@pytest.fixture
def wrong_length() -> str:
    return "Номер недопустимой длинны"


@pytest.fixture
def no_number() -> str:
    return "Не содержит номер"
