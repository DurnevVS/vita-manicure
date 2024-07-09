from typing import Any
from django.contrib import admin
from django import forms
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from rangefilter.filters import DateRangeFilter

from apps.main.models import Window

from .utils.parser import parse_string


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
