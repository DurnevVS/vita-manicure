from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Proxy(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Название"))
    url = models.TextField(verbose_name=_("URL"))

    def __str__(self):
        return self.name
