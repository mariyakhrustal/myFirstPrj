import pandas as pd


def get_csv_transacts(path: str) -> list[dict]:
    """Get transactions from csv"""
    try:
        df = pd.read_csv(path)
        transacts_data = df.to_dict(orient="records")
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


# if __name__ == "__main__":
#     print(get_csv_transacts("data/transactions_csv.csv"))
#     print(get_excel_transacts("data/transactions_excel.xlsx"))
