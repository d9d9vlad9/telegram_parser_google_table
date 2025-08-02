import os
from dotenv import load_dotenv
from zoneinfo import ZoneInfo

load_dotenv()

# ==========================
# Основные настройки
# ==========================
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID", 0))
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
CREDENTIALS_FILE = os.getenv("CREDENTIALS_FILE", "credentials.json")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))

# ==========================
# Настройки логирования
# ==========================
# Уровень логирования: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# ==========================
# Таймзона для сравнения времени задач из Google Sheets с текущим временем
# Укажи свою зону из списка: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
# Примеры: UTC, Europe/Moscow, Asia/Yekaterinburg
# ==========================
TIMEZONE = os.getenv("TIMEZONE", "UTC")
ZONE = ZoneInfo(TIMEZONE)

# ==========================
# Названия листов для таблицы
# ==========================
TABLE_BASE= "ППР"
TABLE_SERVICE = "Служебный"

# ==========================
# Названия колонок для таблицы "TABLE_BASE"
# ==========================
COLUMN_NUMBER = "№ п/п"
COLUMN_WORK_NAME = "Вид работ"
COLUMN_START_TIME = "Запуск"
COLUMN_FINISH_TIME = "Выполнение"

# ==========================
# Названия колонок для таблицы "TABLE_SERVICE"
# ==========================
COLUMN_EMPLOYEE = "Сотрудник"
COLUMN_TELEGRAM = "Telegram"
COLUMN_ACTIVE = "Активность"


# ==========================
# Шаблоны сообщений для уведомлений о регламентных работах
# ==========================

# Сообщение для этапа "start" — когда запланировано начало работ.
# {task_time} — это время, к которому запланирован запуск регламентных работ. Его менять не нужно
MSG_START = "🚀 <b>Запланирован запуск регламентных работ в {task_time}:</b>\n"

# Сообщение для этапа "execution" — когда подошло время выполнения работ.
# {task_time} — это время, к которому нужно начать выполнение регламентных работ. Его менять не нужно
MSG_EXECUTION = "⏱ <b>Подошло время выполнения регламентных работ в {task_time}:</b>\n"