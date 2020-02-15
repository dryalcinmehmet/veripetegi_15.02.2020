from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.views.i18n import JavaScriptCatalog
from django_comments_xtd import LatestCommentFeed
from django.views.generic import ListView
from django.conf.urls.static import static
from .views import *
from django.contrib.auth.views import auth_logout
from django.contrib import auth
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'blog/', include('blog.urls', namespace='blog')),
    path(r'', HomepageView.as_view(),name='homepage'),
    path(r'profile', ProfilePageView.as_view(), name='profile'),
    path(r'dataset-list', DatasetListView.as_view(), name='dataset-list'),
    path(r'dataset-detail', DatasetDetailView.as_view(), name='dataset-detail'),
    path(r'add-dataset', AddDocumentView.as_view(), name='add-dataset'),
    path(r'jupyter', JupyterView.as_view(), name='jupyter'),
    path(r'search', SearchListView.as_view(), name='search'),
    path(r'post-list-filter', PostListView.as_view(), name='post-list-filter'),
    path(r'add-post', AddPostView.as_view(), name='add-post'),
    path(r'author-apply', AuthorApplyView.as_view(), name='author-apply'),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path(r'logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),





    url('^', include('django.contrib.auth.urls')),

    path('q&a-list/', QAListView.as_view(), name='q&a-list'),
    path(r'send-question',AddQAView.as_view(),name='send-question'),
    path(r'qa-detail',QAView.as_view(),name='qa-detail'),

    path(r'comments/', include('django_comments_xtd.urls')),
    path(r'jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(r'feeds/comments/', LatestCommentFeed(), name='comments-feed'),

]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)