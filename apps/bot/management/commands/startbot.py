import asyncio
import logging

from django.core.management.base import BaseCommand

from aiogram import Dispatcher

from apps.bot import bot
from apps.bot.handlers import private_router


class Command(BaseCommand):
    help = 'Starts the bot'

    def handle(self, *args, **options):
        async def start_bot():
            logging.basicConfig(level=logging.INFO)
            dp = Dispatcher()
            dp.include_router(private_router)
            await bot.delete_webhook(drop_pending_updates=True)
            await dp.start_polling(bot)

        asyncio.run(start_bot())
