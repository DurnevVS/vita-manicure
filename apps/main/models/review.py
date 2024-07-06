from django.db import models
from django.utils.translation import gettext_lazy as _


class Review(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Имя'))
    avatar = models.URLField(verbose_name=_('Ссылка на аватар'))
    text = models.TextField(verbose_name=_('Текст отзыва'))
    score = models.IntegerField(verbose_name=_('Оценка (1-5)'))
    rated = models.CharField(max_length=255, verbose_name=_('Дата публикации отзыва'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')
