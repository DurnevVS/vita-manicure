from django import template
register = template.Library()


@register.filter()
def range_(some_int: int):
    return range(0, some_int)
