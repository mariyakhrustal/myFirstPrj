from src.csv_excel_reader import get_csv_transacts, get_excel_transacts
from src.processing import filter_by_state, sort_by_date
from src.sorting_funcs import search_by_string
from src.utils import get_operations_data
from src.widget import get_date, mask_account_card


# Определяем переменную для некорректных вводов.
wrong_output = "Введён некорректный ответ. Повторите ввод."


# Программа приветствует пользователя.
def get_gritting_data():
    """Функциия для приветствия пользователя"""
    print(
        """
Привет! Добро пожаловать в программу работы с банковскими транзакциями!
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из JSON-файла;
2. Получить информацию о транзакциях из CSV-файла;
3. Получить информацию о транзакциях из XLSX-файла.
        """
    )


# Пользователь выбирает файл для обработки транзакций.
def get_transacts_source_data():
    """Функциия для выбора источника транзакций"""
    while True:
        user_input = input("Введите число: ")
        if user_input in ("1", "2", "3"):
            break
        else:
            print(wrong_output)
    menu = {
        "1": "Для обработки выбран JSON-файл.",
        "2": "Для обработки выбран CSV-файл.",
        "3": "Для обработки выбран XLSX-файл.",
    }
    print(f"{menu[user_input]}")
    if user_input == "1":
        transact_list = get_operations_data("../data/operations.json")
    elif user_input == "2":
        transact_list = get_csv_transacts("../data/transactions_csv.csv")
    elif user_input == "3":
        transact_list = get_excel_transacts("../data/transactions_excel.xlsx")
    return transact_list, user_input


# Пользователь выбирает статус интересующих его операций.
def get_state_data(transact_list):
    """Функция для выбора статуса операций"""
    while True:
        print(
            """
Введите статус, по которому необходимо выполнить фильтрацию.
Доступные для фильтровки статусы:  EXECUTED, CANCELED, PENDING
            """
        )
        status_input = input("Введите выбранный статус: ").upper()
        if status_input in ["EXECUTED", "CANCELED", "PENDING"]:
            break
        print(wrong_output)
    state_filtered_data = filter_by_state(transact_list, status_input)
    print(f"Операции отфильтрованы по статусу {status_input}.")
    return state_filtered_data


# Фильтрация по дате.
def get_date_data(state_filtered_data):
    """Функция для выбора фильтрации по дате"""
    while True:
        print("Отфильтровать операции по дате?")
        date_input = input("Введите да/нет: ").lower()
        if date_input in ("да", "нет"):
            break
        print(wrong_output)
    if date_input == "да":
        while True:
            print("Отфильтровать по возрастанию или убыванию?")
            sort_input = input("Введите: по возрастанию / по убыванию: ").lower()
            if sort_input in ("по возрастанию", "по убыванию"):
                break
            print(wrong_output)
        if sort_input == "по возрастанию":
            sort_choice = False
        elif sort_input == "по убыванию":
            sort_choice = True
        sort_filtered_data = sort_by_date(state_filtered_data, sort_choice)
    elif date_input == "нет":
        sort_filtered_data = state_filtered_data
    return sort_filtered_data


# Фильтрация по валюте транзакций
def get_currency_data(sort_filtered_data, user_input):
    """Функция для выбора фильтрации по валюте"""
    while True:
        print("Выводить только рублёвые транзакции?")
        is_rub_input = input("Введите да/нет: ").lower()
        if is_rub_input in ("да", "нет"):
            break
        print(wrong_output)
    if is_rub_input == "да":
        if user_input == "1":
            rub_filtered_data = [
                transact for transact in sort_filtered_data if transact["operationAmount"]["currency"]["code"] == "RUB"
            ]
        else:
            rub_filtered_data = [transact for transact in sort_filtered_data if transact["currency_code"] == "RUB"]
    elif is_rub_input == "нет":
        rub_filtered_data = sort_filtered_data
    return rub_filtered_data


# Фильтрация по определённому слову в описании
def get_filtered_by_word_data(rub_filtered_data):
    """Функция для выбора фильтрации по определенному слову"""
    while True:
        print("Отфильтровать список по определённому слову в описании?")
        str_choice_input = input("Введите да/нет: ").lower()
        if str_choice_input in ("да", "нет"):
            break
        print(wrong_output)
    if str_choice_input == "да":
        word_input = input("Введите слово для сортировки: ").lower()
        word_filtered_data = search_by_string(rub_filtered_data, word_input)
    elif str_choice_input == "нет":
        word_filtered_data = rub_filtered_data
    return word_filtered_data


# Выводим итоговые данные
def get_output_result_data(word_filtered_data, user_input):
    """Функция выводит итоговый результат"""
    total_transacts = len(word_filtered_data)
    if total_transacts > 0:
        print("Распечатываю итоговый список транзакций...\n")
        print(f"Всего банковских операций в выборке {total_transacts}.\n")
        for transaction in word_filtered_data:
            str_date = get_date(transaction["date"])
            description = transaction["description"]
            if user_input == "1":
                summ = transaction["operationAmount"]["amount"]
                currency = transaction["operationAmount"]["currency"]["code"]
            else:
                summ = transaction["amount"]
                currency = transaction["currency_code"]
            if transaction["description"] == "Открытие вклада":
                print(
                    f"""{str_date} {description}
    Сумма: {summ} {currency}\n"""
                )
            else:
                from_whom = mask_account_card(transaction["from"])
                to_whom = mask_account_card(transaction["to"])
                print(
                    f"""{str_date} {description}
    {from_whom} -> {to_whom}
    Сумма: {summ} {currency}\n"""
                )
    else:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации.")


# Запуск программы
def main() -> None:
    """Функция отвечает за основную логику проекта с пользователем и связывает функциональности между собой"""
    # Приветствие пользователя
    get_gritting_data()
    # Получаем данные транзакций в зависимости от выбора пользователя
    transact_list, user_input = get_transacts_source_data()
    # Фильтруем транзакции по статусу
    state_filtered_data = get_state_data(transact_list)
    # Фильтруем транзакции по дате, если требуется
    sort_filtered_data = get_date_data(state_filtered_data)
    # Фильтруем транзакции по валюте (по рублю или нет)
    rub_filtered_data = get_currency_data(sort_filtered_data, user_input)
    # Фильтруем транзакции по слову в описании, если требуется
    word_filtered_data = get_filtered_by_word_data(rub_filtered_data)
    # Выводим итоговые данные
    get_output_result_data(word_filtered_data, user_input)


if __name__ == "__main__":
    main()
