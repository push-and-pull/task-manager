# coding: utf-8
from django.db import models
from tasks.models import Task
from django.core.urlresolvers import reverse


class Tag(models.Model):
    title = models.CharField(unique=True)
    task_list = models.ManyToManyField(Task)

    def __unicode__(self):
        return u'{0} {1}'.format(self.pk, self.title)

    def get_absolute_url(self):
        return reverse('tasks:by_tag', self.title)