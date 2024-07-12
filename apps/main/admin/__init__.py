from .client import ClientAdmin
from .window import WindowAdmin
from .review import ReviewAdmin
from .works import WorksAdmin

from django.contrib import admin

admin.site.index_template = 'admin/base_site.html'