# coding: utf-8

from django.conf.urls import patterns, url

from tasks.views import TaskCreate, TaskList


urlpatterns = patterns(
    '',
    url('^$', TaskList.as_view(), name='my_tasks'),
    url(r'^new$', TaskCreate.as_view(), name='new_task'),
)
