import requests
import asyncio

from django.shortcuts import render
from django.views.generic import View

from .models import Window

from apps.bot import bot

# Create your views here.


class MainPageView(View):

    def get(self, request):
        url = 'https://www.avito.ru/web/6/user/167e9ed21083de7ccd4230e5dda1fc4d/ratings?summary_redesign=1'
        response = requests.get(url).json()
        print(response)
        response = response['entries']
        feedback = {
            'score': response[0]['value']['score'],
            'review_count': response[0]['value']['reviewCount'],
            'reviews': [
                {
                    'name': review['value']['title'],
                    'avatar': review['value']['avatar'],
                    'text': review['value']['textSections'][0]['text'],
                    'score': range(review['value']['score']),
                    'rated': review['value']['rated'],
                }

                for review in response[2:]]
        }
        windows = Window.objects.all()
        return render(request, 'main/index.html', {
            **feedback,
            'windows': windows
        })

    def post(self, request):
        print(request.POST)
        name = request.POST.get("name")
        phone = request.POST.get("phone").replace(' ', '').replace(
            '-', '').replace('(', '').replace(')', '')

        if phone.startswith('8') and len(phone) == 11:
            phone = '+7' + phone[1:]

        window = request.POST.get("window")
        text_to_admin = (
            f'Запись на маникюр:\n'
            f'{name}\n'
            f'{phone}\n'
            f'{window}\n'
        )
        asyncio.run(bot.send_message(915877828, text_to_admin))
        return render(request, 'main/success.html')
