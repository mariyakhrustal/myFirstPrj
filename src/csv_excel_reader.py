import pandas as pd


def get_csv_transacts(path: str) -> list[dict]:
    """Get transactions from csv"""
    try:
        transactions_df = pd.read_csv(path, sep=";", decimal=",", encoding="utf-8")
        transacts_data = transactions_df.to_dict(orient="records")
        return transacts_data
    except FileNotFoundError:
        return []


def get_excel_transacts(path: str) -> list[dict]:
    """Get transactions from excel"""
    try:
        df = pd.read_excel(path)
        transacts_data = df.to_dict(orient="records")
        return transacts_data
    except FileNotFoundError:
        return []
