from django.db import models
from django.utils.translation import gettext_lazy as _


class Works(models.Model):
    url = models.URLField(verbose_name=_("Ссылка на картинку"))

    class Meta:
        verbose_name = _("Мои работы")
        verbose_name_plural = _("Мои работы")

    def __str__(self):
        return self.url
