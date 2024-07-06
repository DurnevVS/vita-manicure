from django.shortcuts import render
from django.views.generic import View

from django_htmx.http import retarget

from .models import Window, Review, Client
from .forms import RegistrationForm

from apps.bot import bot, markup


class MainPageView(View):

    def get(self, request):
        feedback = Review.objects.all()
        form = RegistrationForm()
        return render(request, 'main/index.html', {
            'reviews': feedback,
            'form': form
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

            bot.send_message(915877828, text_to_admin, reply_markup=markup(window.id))

            response = render(request, 'main/success.html')

            return retarget(response, '#body')

        else:
            return render(request, 'main/includes/index/form.html', {'form': form})
