from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag()
def render_image(image_url, alt_text='', css_class='img-fluid'):
    if image_url:
        return mark_safe(f'<img src="{image_url}" alt="{alt_text}" class="{css_class}">')
    else:
        return ''
