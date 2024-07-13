from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from apps.main.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):

    def times_come(self, obj):
        return obj.windows.filter(done=True).count()

    times_come.short_description = _('Количество посещений')
    list_display = ('name', 'phone', 'times_come', 'blocked')
    search_fields = ('name', 'phone')
    list_per_page = 20
