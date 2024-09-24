from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def render_image(image, alt_text='', css_class='img-fluid'):
    if image:
        return mark_safe(f'<img src="{image}" alt="{alt_text}" class="{css_class}">')
    else:
        return ''
