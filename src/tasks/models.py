# coding: utf-8

from django.db import models
from django.core.exceptions import ValidationError

from users.models import User


class Task(models.Model):

    TASK_STATUS = (
        (0, 'open'),
        (1, 'resolved')
    )

    created_by = models.ForeignKey(to=User, verbose_name='Created by')
    title = models.CharField(verbose_name='Title', max_length=200)
    description = models.TextField(verbose_name='Description', blank=True)
    status = models.IntegerField(choices=TASK_STATUS)

    created_at = models.DateTimeField(auto_now=False, auto_now_add=False)
    due_date = models.DateTimeField()

    def __unicode__(self):
        return u'{0} {1}'.format(self.pk, self.title)

    def clean(self):
        if self.due_date <= self.created_at:
            raise ValidationError('due date must be greater than current time')
