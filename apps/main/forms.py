from string import punctuation, whitespace
from typing import Any

from django import forms
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Window


def format_phone(value):
    characters_to_remove = punctuation.replace('+', '') + whitespace
    value = ''.join(i for i in value if i not in characters_to_remove)
    if value.startswith('8'):
        return '+7' + value[1:]
    return value


def validate_phone_lenght(value):
    if len(value) != 12:
        raise ValidationError('Некорректный номер')


def validate_phone(value):
    if not value[1:].isdigit():
        raise ValidationError('Только цифры')


class PhoneField(forms.CharField):

    def to_python(self, value: str) -> str:
        return format_phone(value)

    def validate(self, value: Any) -> None:
        super().validate(value)
        validate_phone(value)
        validate_phone_lenght(value)


class RegistrationForm(forms.Form):
    name = forms.CharField(required=True)
    phone = PhoneField(required=True)
    window = forms.ModelChoiceField(
        queryset=Window.objects.filter(client=None).order_by('date'),
        empty_label=_('Выберите окошко'),
    )
