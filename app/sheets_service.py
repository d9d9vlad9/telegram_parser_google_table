import gspread
from .config import SPREADSHEET_ID, CREDENTIALS_FILE, TABLE_BASE, TABLE_SERVICE


class SheetsService:
    """
    Сервис для работы с Google Sheets через библиотеку gspread.

    Атрибуты:
        gc: объект клиента gspread, аутентифицированный через сервисный аккаунт.
        sheet_tasks: лист с задачами (название листа задаётся через TABLE_BASE).
        sheet_employees: лист с данными сотрудников (название листа задаётся через TABLE_SERVICE).

    Методы:
        get_tasks() - возвращает все данные из листа с задачами в виде списка списков.
        get_employees() - возвращает все данные из листа с сотрудниками в виде списка словарей.
    """
    def __init__(self):
        self.gc = gspread.service_account(filename=CREDENTIALS_FILE)
        self.sheet_tasks = self.gc.open_by_key(SPREADSHEET_ID).worksheet(TABLE_BASE)
        self.sheet_employees = self.gc.open_by_key(SPREADSHEET_ID).worksheet(TABLE_SERVICE)

    def get_tasks(self):
        """
        Получить все данные из листа с задачами.

        Возвращает:
            list[list[str]]: Все значения из листа задач,
            где каждая строка — это список значений ячеек.
        """
        return self.sheet_tasks.get_all_values()

    def get_employees(self):
        """
        Получить все данные из листа с сотрудниками.

        Возвращает:
            list[dict]: Все записи сотрудников в виде списка словарей,
            где ключи — названия колонок, а значения — данные ячеек.
        """
        return self.sheet_employees.get_all_records()
