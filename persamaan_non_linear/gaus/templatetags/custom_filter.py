from django import template

register = template.Library()

@register.filter
def format_number(value):
    # Jika value adalah bilangan bulat (2.0 -> 2), maka buang desimalnya
    if value % 1 == 0:
        return int(value)
    # Jika value memiliki desimal lain (2.5), maka biarkan
    return value
