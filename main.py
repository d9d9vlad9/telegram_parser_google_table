import asyncio
from app.bot import create_bot
from app.sheets_service import SheetsService
from app.notifier import Notifier
from app.scheduler import Scheduler
from app.config import LOG_LEVEL
import logging

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.INFO),
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%d.%m.%Y %H:%M:%S'
)

async def main():
    bot, dp = create_bot()
    sheets = SheetsService()
    notifier = Notifier(bot)
    scheduler = Scheduler(notifier, sheets)

    asyncio.create_task(scheduler.run())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
