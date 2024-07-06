from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
from .client import Client

import locale
locale.setlocale(
    category=locale.LC_ALL,
    locale="Russian"  # Note: do not use "de_DE" as it doesn't work
)


class Window(models.Model):
    date = models.DateTimeField(verbose_name=_('Окошко'))
    done = models.BooleanField(verbose_name=_('Выполнено'), default=False)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name='windows',
        verbose_name=_('Клиент'), null=True, blank=True
    )

    def __str__(self):
        return self.date.strftime('%a %d %B %Y - %H:%M')

    class Meta:
        verbose_name = _('Окошко')
        verbose_name_plural = _('Окошки')
