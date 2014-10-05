# coding: utf-8

from django.db import models
from django.core.exceptions import ValidationError

from users.models import User


class Task(models.Model):

    class TASK_STATUS(object):
        OPEN = 0
        RESOLVED = 1

        VALUES = {
            OPEN: 'open',
            RESOLVED: 'resolved'
        }

    created_by = models.ForeignKey(to=User, verbose_name='Created by')
    title = models.CharField(verbose_name='Title', max_length=200)
    description = models.TextField(verbose_name='Description', blank=True)
    status = models.IntegerField(choices=TASK_STATUS.VALUES.items())

    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()

    def __unicode__(self):
        return u'{0} {1}'.format(self.pk, self.title)

    def clean(self):
        if self.due_date <= self.created_at:
            raise ValidationError('due date must be greater than current time')
