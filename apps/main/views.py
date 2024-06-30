import asyncio

from django.shortcuts import render
from django.views.generic import View

from .models import Window, Review

from apps.bot import bot

# Create your views here.


class MainPageView(View):

    def get(self, request):
        feedback = Review.objects.all()
        windows = Window.objects.all()
        return render(request, 'main/index.html', {
            'reviews': feedback,
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
