from aiogram import Router, types, F
from aiogram.filters import Command

import requests

from apps.main.models import Window, Review

from datetime import datetime

private_router = Router()


@private_router.message(Command('start'))
async def start(message: types.Message):
    user_id = message.from_user.id
    print(user_id)
    await message.answer('Готов к работе!\n Отправьте расписание окошек!')


@private_router.message(Command('reviews'))
async def get_reviews(message: types.Message):
    url = 'https://www.avito.ru/web/6/user/167e9ed21083de7ccd4230e5dda1fc4d/ratings?summary_redesign=1'
    response = requests.get(url).json()
    response = response['entries']
    feedback = [
        {
            'name': review['value']['title'],
            'avatar': review['value']['avatar'],
            'text': review['value']['textSections'][0]['text'],
            'score': review['value']['score'],
            'rated': review['value']['rated'],
        }
        for review in response[2:]
    ]

    await Review.objects.all().adelete()

    for review in feedback:
        await Review.objects.acreate(**review)

    await message.answer('Отзывы обновлены!')


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
