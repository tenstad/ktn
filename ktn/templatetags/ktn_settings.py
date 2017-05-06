from django import template
from django.conf import settings

register = template.Library()

@register.filter(name='setting')
def setting(name):
    return getattr(settings, name, "")
