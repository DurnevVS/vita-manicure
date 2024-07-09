from django.db import models
from django.utils.translation import gettext_lazy as _


class Works(models.Model):
    image = models.ImageField(_("Изображение"), upload_to="my_works")

    class Meta:
        verbose_name = _("Мои работы")
        verbose_name_plural = _("Мои работы")

    def __str__(self):
        return self.name
