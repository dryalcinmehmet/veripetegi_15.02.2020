from django.conf.urls import url, include
from django.urls import path
from django.views.generic import ListView, DateDetailView

from blog.models import Post, QA


app_name = 'blog'


urlpatterns = [

    url(r'^accounts/', include('django.contrib.auth.urls')),
    # url(r'^$', ListView.as_view(model=Post, paginate_by=15), name='post-list'),

    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        DateDetailView.as_view(date_field="publish", model=Post),
        name='post-detail'),



]
