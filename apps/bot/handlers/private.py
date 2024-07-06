import telebot
from telebot import types

from apps.main.models import Window


def private_router(bot: telebot.TeleBot):

    @bot.message_handler(commands=['start', 'help'])
    def start(message: types.Message):

        text = (
            '1. Кнопка "Подтвердить" - запись клиента остается\n'
            '2. Кнопка "Отменить" - запись клиента удаляется\n'
            '3. Кнопка "Заблокировать" - запись клиента удаляется и номер заносится в черный список\n'
        )

        bot.send_message(message.chat.id, text)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('apply'))
    def apply(call: types.CallbackQuery):
        bot.send_message(call.message.chat.id, "Запись подтверждена")

    @bot.callback_query_handler(func=lambda call: call.data.startswith('cancel'))
    def cancel(call: types.CallbackQuery):
        window_id = call.data.split('-')[1]
        window = Window.objects.get(id=window_id)
        window.client = None
        window.save()
        bot.send_message(call.message.chat.id, "Запись отменена")

    @bot.callback_query_handler(func=lambda call: call.data.startswith('block'))
    def block(call: types.CallbackQuery):
        window_id = call.data.split('-')[1]
        window = Window.objects.get(id=window_id)
        client = window.client
        client.blocked = True
        client.save()
        window.client = None
        window.save()
        bot.send_message(call.message.chat.id, "Запись отменена и номер добавлен в черный список")
