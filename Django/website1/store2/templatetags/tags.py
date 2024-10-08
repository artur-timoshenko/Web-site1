from collections.abc import Iterable

from django import template

register = template.Library()


@register.filter
def add(x, y):
    return x + y


@register.filter
def subtract(x, y):
    return x - y


@register.filter
def multiply(x, y):
    return x * y


@register.filter
def divide(x, y):
    return x / y


@register.filter
def salePrice(price, salePercent):
    if salePercent == 0:
        return price
    else:
        return price * (1 - salePercent / 100)
