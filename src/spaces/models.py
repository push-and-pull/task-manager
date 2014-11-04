# coding: utf-8

from django.db import models
from users.models import User
from tasks.models import Task
from django.core.urlresolvers import reverse


class Space(models.Model):
    name = models.CharField(max_length=150)
    created_by = models.ForeignKey(to=User, verbose_name='Created by', related_name='space_created_by')
    users = models.ManyToManyField(User, related_name='users')
    tasks = models.ManyToManyField(Task)

    def __unicode__(self):
        return u'{0} {1}'.format(self.pk, self.name)

    def get_absolute_url(self):
        return reverse('space:space_detail', args=(self.pk,))
