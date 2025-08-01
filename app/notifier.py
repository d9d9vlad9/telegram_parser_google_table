from aiogram import Bot
from .config import GROUP_ID


class Notifier:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def send_group_message(self, text: str):
        await self.bot.send_message(GROUP_ID, text)
