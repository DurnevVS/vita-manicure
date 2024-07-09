import os

from django.shortcuts import render
from django.views.generic import View

from django_htmx.http import retarget

from apps.bot import bot, markup

from .models import Window, Review, Client, Works
from .forms import RegistrationForm


class MainPageView(View):

    def get(self, request):
        return render(request, 'main/index.html', {
            'works': Works.objects.all(),
            'reviews': Review.objects.all(),
            'form': RegistrationForm(),
        })

    def post(self, request):

        form = RegistrationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            client, created = Client.objects.get_or_create(
                phone=phone,
                defaults={
                    'name': name,
                    'phone': phone,
                }
            )
            if client.blocked:
                response = render(request, 'main/success.html', {'blocked': True})
                return retarget(response, '#body')

            window = Window.objects.get(id=request.POST['window'])
            window.client = client
            window.save()

            text_to_admin = (
                f'Запись на маникюр:\n'
                f'{name}\n'
                f'{phone}\n'
                f'{window}\n'
            )
            if created:
                text_to_admin += 'Новый клиент'

            send_admins(text_to_admin, markup(window.id))

            response = render(request, 'main/success.html')

            return retarget(response, '#body')

        else:
            return render(request, 'main/includes/index/form.html', {'form': form})


def send_admins(message, markup):
    for admin in os.environ.get("TG_ADMINS").split(","):
        bot.send_message(int(admin), message, reply_markup=markup)
