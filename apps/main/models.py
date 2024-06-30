from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Window(models.Model):
    time = models.DateTimeField(verbose_name=_('Окошко'))
    approved = models.BooleanField(verbose_name=_('Одобрено'), default=False)

    def __str__(self):
        return self.time

    class Meta:
        verbose_name = _('Окошко')
        verbose_name_plural = _('Окошки')


class Review(models.Model):
    name = models.CharField(max_length=255)
    avatar = models.URLField()
    text = models.TextField()
    score = models.IntegerField()
    rated = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')
