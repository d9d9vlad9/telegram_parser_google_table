from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from .config import BOT_TOKEN


def create_bot():
    """
    Создаёт и возвращает экземпляры бота и диспетчера aiogram.

    Возвращает:
        tuple:
            bot (Bot): объект Telegram-бота с заданным токеном и настройками.
            dp (Dispatcher): диспетчер для обработки событий и команд бота.

    Особенности:
        - Используется токен из конфигурации BOT_TOKEN.
        - Для бота установлен режим парсинга HTML-сообщений (parse_mode="HTML").
        - Диспетчер инициализируется с настройками по умолчанию.
    """
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()
    return bot, dp
