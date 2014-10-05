# coding: utf-8

from django.conf.urls import patterns, url
from views import user_register
urlpatterns = patterns(
    '',
    url(r'^sign_in$', user_register, name='sign_in')
)