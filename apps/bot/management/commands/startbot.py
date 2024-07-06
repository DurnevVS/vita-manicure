
from django.core.management.base import BaseCommand


from apps.bot import bot
from apps.bot.handlers import private_router


class Command(BaseCommand):
    help = 'Starts the bot'

    def handle(self, *args, **options):

        private_router(bot)
        bot.infinity_polling()
