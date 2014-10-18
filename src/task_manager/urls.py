# coding: utf-8

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import patterns, include, url
from django.conf import settings

# from django.contrib import admin

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'task_manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
    url(r'^tasks/', include('tasks.urls', namespace='tasks')),
    url(r'^user/', include('users.urls', namespace='users')),
)

if settings.DEBUG:
    urlpatterns += patterns(
        'django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )
