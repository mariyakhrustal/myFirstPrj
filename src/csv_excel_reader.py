import csv


def get_csv_transacts(path: str) -> list:
    """Get transactions from csv"""
    try:
        with open(path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
            if data:
                return data
            return []
    except FileNotFoundError:
        return []


if __name__ == "__main__":
    print(get_csv_transacts("../data/transactions_csv.csv"))
