class TaskProcessor:
    """
    Класс для обработки и фильтрации задач по активности и группировке.

    Attributes:
        active_column (str): Имя колонки, по которой определяется активность задачи.
    """
    def __init__(self, active_column: str):
        self.active_column = active_column

    def filter_active_tasks(self, tasks: list) -> list:
        """
        Фильтрует задачи, которые активны сейчас.

        Args:
            tasks (list): Список задач (dict), каждая должна содержать ключ active_column.

        Returns:
            list: Отфильтрованный список задач, у которых active_column == "1".
        """
        return [t for t in tasks if t.get(self.active_column) == "1"]

    @staticmethod
    def group_tasks(tasks: list) -> dict:
        """
        Группирует задачи по ключу (stage, time).

        Args:
            tasks (list): Список активных задач, каждая задача — dict с ключами "stage", "time" и "work_name".

        Returns:
            dict: Словарь, где ключ — кортеж (stage, time), а значение — список названий задач (work_name).
        """
        grouped = {}
        for task in tasks:
            key = (task["stage"], task["time"])
            grouped.setdefault(key, []).append(task["work_name"])
        return grouped
