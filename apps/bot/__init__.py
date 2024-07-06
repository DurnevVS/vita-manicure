import os
from telebot import TeleBot
from telebot.util import quick_markup


bot = TeleBot(os.environ.get('BOT_TOKEN'))


def markup(window_id: str):

    return quick_markup({
        'Подтвердить': {'callback_data': f'apply-{window_id}'},
        'Отменить': {'callback_data': f'cancel-{window_id}'},
        'Заблокировать': {'callback_data': f'block-{window_id}'}
    }, row_width=2)
