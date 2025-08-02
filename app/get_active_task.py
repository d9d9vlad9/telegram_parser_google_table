from datetime import datetime
from zoneinfo import ZoneInfo
import logging
from .config import (
    COLUMN_NUMBER,
    COLUMN_WORK_NAME,
    COLUMN_START_TIME,
    COLUMN_FINISH_TIME,
    ZONE,
)


logger = logging.getLogger(__name__)

def parse_time(t: str):
    """Парсит время в формате ЧЧ:ММ, возвращает datetime или None."""
    try:
        return datetime.strptime(t.strip(), "%H:%M") if t else None
    except (ValueError, AttributeError):
        return None

def get_active_tasks_for_now(data):
    """
    Обрабатывает данные таблицы с задачами, находит задачи,
    активные в текущий момент времени по дате и времени.

    Параметры:
    - data: список списков, каждая внутренняя структура - строка таблицы.

    Возвращает список словарей с активными задачами и информацией о них.
    """
    if len(data) < 3:
        logger.warning("Мало строк в таблице")
        return []

    date_row = data[1]
    header = data[0]
    today_str = datetime.now(ZoneInfo("UTC")).astimezone(ZONE).strftime("%d.%m.%Y")
    logger.info(f"Ищем колонку с сегодняшней датой: {today_str}")

    def find_col_index(head, col_name):
        """
        Вспомогательная функция для поиска индекса колонки по имени.
        Возвращает индекс или -1, если колонка не найдена.
        """
        try:
            res = head.index(col_name)
            if res:
                logger.debug(f"Нашли колонку {col_name}")
                return res
        except ValueError:
            logger.debug(f"Ошибка не нашли колонку с именем {col_name}")
            return -1

    number_name_col = find_col_index(header, COLUMN_NUMBER)
    work_name_col = find_col_index(header, COLUMN_WORK_NAME)
    start_time_col = find_col_index(header, COLUMN_START_TIME)
    finish_time_col = find_col_index(header, COLUMN_FINISH_TIME)

    date_col = None
    for i in range(4, len(date_row)):
        logger.debug(f"Проверяем колонку {i} с заголовком '{date_row[i]}'")
        if date_row[i] == today_str:
            date_col = i
            logger.info(f"Найдена колонка с датой {today_str} под индексом {date_col}")
            break

    if date_col is None:
        logger.warning(f"Столбец с датой {today_str} не найден")
        return []

    now_str = datetime.now(ZoneInfo("UTC")).astimezone(ZONE).strftime("%H:%M")
    logger.info(f"Текущее время для сравнения: {now_str}")
    utc_now = datetime.now(ZoneInfo("UTC")).strftime("%H:%M")
    logger.debug(f"Текущее UTC: {utc_now}, локальное: {now_str}, зона: {ZONE}")

    active_tasks = []

    for idx, row in enumerate(data[2:], start=3):
        number_name = row[number_name_col].strip() if number_name_col != -1 and len(row) > number_name_col else ""
        work_name = row[work_name_col].strip() if work_name_col != -1 and len(row) > work_name_col else ""

        if not number_name and not work_name:
            logger.info(f"Пустые колонки '{COLUMN_NUMBER}' и '{COLUMN_WORK_NAME}' в строке {idx}, прекращаем обработку")
            break

        task_date_cell = row[date_col].strip() if len(row) > date_col else ""
        start_time = row[start_time_col].strip() if start_time_col != -1 and len(row) > start_time_col else ""
        finish_time = row[finish_time_col].strip() if finish_time_col != -1 and len(row) > finish_time_col else ""

        logger.debug(
            f"Строка {idx}: {COLUMN_WORK_NAME}='{work_name}', {COLUMN_START_TIME}='{start_time}', "
            f"{COLUMN_FINISH_TIME}='{finish_time}', Активность по дате='{task_date_cell}'"
        )

        if task_date_cell == "1":
            if start_time == now_str:
                active_tasks.append({
                    "work_name": work_name,
                    "time": start_time,
                    "date": task_date_cell,
                    "stage": "start"
                })

            if finish_time == now_str:
                active_tasks.append({
                    "work_name": work_name,
                    "time": finish_time,
                    "date": task_date_cell,
                    "stage": "finish"
                })

    logger.info(f"Всего активных задач на сейчас: {len(active_tasks)}")
    return active_tasks
