# coding: utf-8

from django.conf.urls import patterns, url
from tags.views import TaskListByTag



urlpatterns = patterns(
    '',
    url(r'^(?P<tag_name>\w)$', TaskListByTag.as_view(), name='task_detail'),
)
