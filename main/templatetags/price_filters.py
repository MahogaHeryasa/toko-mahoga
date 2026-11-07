from decimal import Decimal, InvalidOperation

from django import template


register = template.Library()


@register.filter
def rupiah(value):
    try:
        amount = Decimal(str(value)).quantize(Decimal("1"))
    except (InvalidOperation, TypeError, ValueError):
        return value

    return f"{amount:,}".replace(",", ".")
