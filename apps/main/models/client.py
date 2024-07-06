from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Имя'))
    phone = models.CharField(max_length=255, verbose_name=_('Телефон'))
    blocked = models.BooleanField(default=False, verbose_name=_('Заблокирован'))

    def __str__(self):
        return f'{self.name} - {self.phone}'

    class Meta:
        verbose_name = _('Клиент')
        verbose_name_plural = _('Клиенты')
