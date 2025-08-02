import datetime
import asyncio
import json
import logging
from .config import CHECK_INTERVAL, COLUMN_ACTIVE, COLUMN_TELEGRAM, MSG_START, MSG_EXECUTION, ZONE
from .employee_notifier import EmployeeNotifier
from .get_active_task import get_active_tasks_for_now
from .sheets_service import SheetsService
from .notifier import Notifier
from .task_processor import TaskProcessor
from zoneinfo import ZoneInfo


logger = logging.getLogger(__name__)


class Scheduler:
    """
    Класс Scheduler управляет циклической проверкой регламентных работ,
    формирует уведомления и отправляет их через заданный Notifier.

    Attributes:
        notifier (Notifier): Отправитель сообщений.
        sheets (SheetsService): Сервис для получения данных из таблиц.
        already_notified (set): Множество уже отправленных уведомлений.
        task_processor (TaskProcessor): Обработка и фильтрация задач.
        employee_notifier (EmployeeNotifier): Формирование упоминаний сотрудников.
    """
    def __init__(self, notifier: Notifier, sheets: SheetsService):
        """
        Инициализация Scheduler.

        Args:
            notifier (Notifier): Объект для отправки сообщений.
            sheets (SheetsService): Сервис для работы с таблицами.
        """
        self.notifier = notifier
        self.sheets = sheets
        self.already_notified = set()
        self.task_processor = TaskProcessor("date")
        self.employee_notifier = EmployeeNotifier(COLUMN_ACTIVE, COLUMN_TELEGRAM)
        logger.info("Scheduler initialized")

    async def run(self):
        """
        Запускает главный цикл работы Scheduler.

        Периодически проверяет задачи и отправляет уведомления.
        """
        logger.info("Scheduler started")
        await self.send_welcome_message()

        while True:
            try:
                await self.check_tasks()
            except Exception as e:
                logger.error(f"Ошибка в check_tasks: {e}", exc_info=True)
            await asyncio.sleep(CHECK_INTERVAL)

    async def send_welcome_message(self):
        """
        Отправляет приветственное сообщение при запуске бота.
        """
        now = datetime.datetime.now(ZoneInfo("UTC")).astimezone(ZONE).strftime("%d.%m.%Y %H:%M")
        text = (
            f"🤖 <b>Бот запущен и готов к работе!</b>\n"
            f"Сегодня: <b>{now}</b>\n\n"
            f"Я буду уведомлять о запланированных и текущих регламентных работах в соответствии с расписанием."
        )
        await self.notifier.send_group_message(text)

    async def check_tasks(self):
        """
        Выполняет проверку текущих активных задач,
        группирует их и отправляет уведомления ответственным сотрудникам.
        """
        data = self.sheets.get_tasks()
        employees = self.sheets.get_employees()

        tasks_now = get_active_tasks_for_now(data)
        logger.info(f"Активные задачи:\n{json.dumps(tasks_now, ensure_ascii=False, indent=2)}")
        active_tasks = self.task_processor.filter_active_tasks(tasks_now)
        if not active_tasks:
            logger.debug("В данное время задач для уведомления нет")
            return

        grouped_tasks = self.task_processor.group_tasks(active_tasks)
        mentions = self.employee_notifier.get_mentions(employees)

        for (stage, task_time), tasks in grouped_tasks.items():
            message = self._build_message(stage, task_time, tasks, mentions)
            notify_key = f"{stage}:{task_time}"
            if notify_key in self.already_notified:
                continue

            await self.notifier.send_group_message(message)
            self.already_notified.add(notify_key)

    @staticmethod
    def _build_message(stage: str, task_time: str, tasks: list, mentions: list) -> str:
        """
        Формирует текст уведомления по группе задач.

        Args:
            stage (str): Стадия задачи ('start' или 'execution').
            task_time (str): Время задачи.
            tasks (list): Список названий задач.
            mentions (list): Список упоминаний сотрудников.

        Returns:
            str: Сформированное сообщение для отправки.
        """
        if stage == "start":
            title = MSG_START.format(task_time=task_time)
        else:
            title = MSG_EXECUTION.format(task_time=task_time)

        task_lines = "\n".join(f"- {t}" for t in tasks)
        return f"{title}{task_lines}\n\nОтветственные: {', '.join(mentions)}"

