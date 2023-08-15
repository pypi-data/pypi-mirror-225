from django import template

register = template.Library()

@register.filter
def order_by(queryset):
    return queryset.order_by('pk', 'year')

@register.filter
def subs_total_earn(a, b):
    return a - b