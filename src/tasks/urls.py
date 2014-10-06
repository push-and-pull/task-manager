# coding: utf-8

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from tasks.views import TaskCreate


urlpatterns = patterns(
    '',
    url('^$', TemplateView.as_view(template_name='task/index.html'), name='my_tasks'),
    url(r'^new$', TaskCreate.as_view(), name='new_task')
)
