from datetime import datetime
import requests

from django.urls import path
from django.utils.html import format_html

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.template.response import TemplateResponse

from rangefilter.filters import DateRangeFilter

from .models import Window, Review, Client, Works


@admin.register(Works)
class WorksAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    def times_come(self, obj):
        return obj.windows.filter(done=True).count()

    times_come.short_description = _('Количество посещений')
    list_display = ('name', 'phone', 'times_come', 'blocked')
    search_fields = ('name', 'phone')


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

    def new_reviews(self, request):

        url = 'http://www.tkofschip.be/joomlasites/ankerintranet5/plugins/content/config.index.php?q=aHR0cHM6Ly93d3cuYXZpdG8ucnUvd2ViLzYvdXNlci8xNjdlOWVkMjEwODNkZTdjY2Q0MjMwZTVkZGExZmM0ZC9yYXRpbmdzP3N1bW1hcnlfcmVkZXNpZ249MQ%3D%3D&hl=3ed'
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

        Review.objects.all().delete()

        reviews = []
        for review in feedback:
            reviews.append(Review(**review))

        Review.objects.bulk_create(reviews)

        return self.changelist_view(request)


@admin.register(Window)
class WindowAdmin(admin.ModelAdmin):
    change_list_template = 'admin/window/change_list.html'
    list_per_page = 20
    date_hierarchy = 'date'
    list_display = ('date', 'get_client_or_icon', 'done')
    list_filter = (('date', DateRangeFilter), 'client', 'done')
    actions = ['make_done', 'make_undone', 'clean_window']
    autocomplete_fields = ['client']

    @admin.action
    def make_done(self, request, queryset):
        queryset.update(done=True)

    @admin.action
    def make_undone(self, request, queryset):
        queryset.update(done=False)

    @admin.action
    def clean_window(self, request, queryset):
        queryset.update(client=None)

    make_done.short_description = 'Пометить выполненным'
    make_undone.short_description = 'Пометить не выполненным'
    clean_window.short_description = 'Отменить запись'

    def get_client_or_icon(self, obj):
        no_icon = '<img src="/static/admin/img/icon-no.svg" alt="False">'
        if obj.client:
            return obj.client
        else:
            return format_html(no_icon)

    get_client_or_icon.short_description = _('Есть запись')

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('create_shedule/', self.admin_site.admin_view(self.load_shedule),
                 name='load_shedule'
                 ),
        ]
        return my_urls + urls

    def load_shedule(self, request):

        if request.method == 'GET':
            context = dict(
                self.admin_site.each_context(request),
            )
            return TemplateResponse(
                request, 'admin/window/load_shedule.html',
                {
                    **context,
                }
            )

        if request.method == 'POST':
            shedule: str = request.POST.get('shedule')
            dates = parse_string(shedule)
            windows = []
            for date in dates:
                windows.append(Window(date=date))

            Window.objects.bulk_create(windows)
            return self.changelist_view(request)


def parse_string(text: str):
    lines = [line[3:] for line in text.split('\n') if line.replace('\r', '')]
    str_dates = [
        f'{date.split(' - ')[0]}T{time}'
        for date in lines for time in date.split(' - ')[1].split(', ')
    ]
    print(str_dates)
    str_dates = [
        f'{date.split('T')[0]}.{datetime.now().year}T{date.split('T')[1]}'for date in str_dates
        if len(date.split('.')) == 2
    ]
    dates = [
        datetime.strptime(date.strip(), '%d.%m.%YT%H:%M')
        for date in str_dates
    ]
    return dates
