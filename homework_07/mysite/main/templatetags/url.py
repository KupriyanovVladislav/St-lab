from django import template
from django.utils.html import format_html
from django.urls import reverse


register = template.Library()


@register.filter
def url(value):
    result = reverse('item_update', args=[value.department.shop_id, value.department_id, value.id])
    return format_html(f"<a href='{result}'>{value}</a>")
