from aiogram import Router, types, F
from aiogram.filters import Command

from apps.main.models import Window

from datetime import datetime

private_router = Router()


def parse_message(text: str):
    lines = [line[2:] for line in text.split('\n') if line]
    str_dates = [
        f'{date.split(' - ')[0]}T{time}'
        for date in lines for time in str(date.split(' - ')[1]).split(', ')
    ]
    dates = [
        datetime.strptime(date.strip(), '%d.%mT%H:%M')
        for date in str_dates
    ]
    return dates


@private_router.message(Command('start'))
async def start(message: types.Message):
    user_id = message.from_user.id
    print(user_id)
    await message.answer('Готов к работе!\n Отправьте расписание окошек!')


@private_router.message(F.text)
async def create_schedule(message: types.Message):
    try:
        Window.objects.all().adelete()
        dates = parse_message(message.text)
        for date in dates:
            await Window.objects.acreate(time=date, approved=False)
        await message.answer('Расписание создано!')
    except:
        await message.answer('Что-то пошло не так...')
