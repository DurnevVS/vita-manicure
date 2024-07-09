import requests
from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _

from apps.proxy.models import Proxy

from apps.main.models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_per_page = 20
    change_list_template = 'admin/review/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path(
                'new_reviews/', self.admin_site.admin_view(self.new_reviews),
                name='new_reviews'),
        ]
        return my_urls + urls

    # Подумать нужно ли рефакторить
    def new_reviews(self, request):
        urls = Proxy.objects.values_list('url', flat=True)
        try:
            for url in urls:
                try:
                    response = requests.get(url).json()
                    response = response['entries']
                except:
                    continue
                break

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

            Review.objects.all().delete()

            reviews = []
            for review in feedback:
                reviews.append(Review(**review))

            Review.objects.bulk_create(reviews)
        except:
            pass
        return self.changelist_view(request)
