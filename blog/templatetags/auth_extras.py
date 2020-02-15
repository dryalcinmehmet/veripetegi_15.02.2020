from django import template
from django.contrib.auth.models import Group
# from blog.models import QA

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

#
# @register.filter(name='has_fixed')
# def has_fixed(fixed, status):
#     group = QA.objects.get(fixed=status)
#     return True if group in fixed.groups.all() else False