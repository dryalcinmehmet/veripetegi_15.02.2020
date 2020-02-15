from django import template
import blog.models as CustomModels
from django.contrib.auth.models import User



register = template.Library()

@register.simple_tag(takes_context=True)
def get_profile(context,user):

    profile=CustomModels.CustomProfile.objects.get(user=User.objects.get(username=user))
    return profile


@register.simple_tag(takes_context=True)
def get_post_title(context,title):
    post_title=CustomModels.Post.objects.get(title=title)
    return post_title


@register.simple_tag(takes_context=True)
def get_document_title(context,title):
    document_title=CustomModels.Document.objects.get(title=title)
    return document_title