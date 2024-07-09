from django.contrib import admin
from django.utils.translation import gettext_lazy as _


from apps.main.models import Works


@admin.register(Works)
class WorksAdmin(admin.ModelAdmin):
    pass