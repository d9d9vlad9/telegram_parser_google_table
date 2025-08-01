import logging


class EmployeeNotifier:
    """
    Класс для формирования списка упоминаний сотрудников для уведомлений.
    """
    def __init__(self, active_key: str, telegram_key: str):
        self.active_key = active_key
        self.telegram_key = telegram_key
        self.logger = logging.getLogger(__name__)

    def get_mentions(self, employees: list) -> list:
        """
        Формирует список упоминаний для активных сотрудников.

        Args:
            employees (list): Список словарей с данными сотрудников.

        Returns:
            list: Список строк с Telegram упоминаниями (например, '@username' или '123456789').
        """
        mentions = []
        for emp in employees:
            if str(emp.get(self.active_key, "")).strip().upper() == "TRUE":
                tg = str(emp.get(self.telegram_key, "")).strip()
                if tg:
                    mentions.append(tg if tg.isdigit() else f"@{tg}")
        self.logger.debug(f'Список активных сотрудников: {' '.join(mentions)}')
        return mentions
