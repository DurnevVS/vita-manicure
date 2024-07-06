from django import template
register = template.Library()


@register.filter()
def range_(some_int: int):
    if some_int is None:
        some_int = 0
    return range(0, some_int)
