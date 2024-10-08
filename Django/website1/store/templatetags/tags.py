from collections.abc import Iterable

from django import template

register = template.Library()


@register.filter
def test(object: Iterable):
    return object
