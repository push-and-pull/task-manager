# coding: utf-8

from django.conf.urls import patterns, url
from views import user_register, user_login, user_logout
urlpatterns = patterns(
    '',
    url(r'^sign_in$', user_register, name='sign_in'),
    url(r'^login', user_login, name='login'),
    url(r'^logout', user_logout, name='logout')
)