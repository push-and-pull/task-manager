# coding: utf-8
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from users.models import User
from spaces.models import Space


class Task(models.Model):

    class TASK_STATUS(object):
        OPEN = 0
        RESOLVED = 1

        VALUES = {
            OPEN: 'open',
            RESOLVED: 'resolved'
        }

    created_by = models.ForeignKey(to=User, verbose_name='Created by', related_name='created_by')
    assigned_to = models.ForeignKey(to=User, verbose_name='Assigned to', related_name='assigned_to',
                                    default=created_by)
    space = models.ForeignKey(to=Space, verbose_name='space', null=True)
    title = models.CharField(verbose_name='Title', max_length=200)
    description = models.TextField(verbose_name='Description', blank=True)
    status = models.IntegerField(choices=TASK_STATUS.VALUES.items())
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()

    def __unicode__(self):
        return u'{0} {1}'.format(self.pk, self.title)

    def get_absolute_url(self):
        return reverse('tasks:task_detail', args=(self.pk,))

    def clean(self):
        if self.due_date <= timezone.now().date():
            raise ValidationError('due date must be greater than current time')


class Tag(models.Model):
    title = models.CharField(unique=True, max_length=100)
    task_list = models.ManyToManyField(Task)

    def __unicode__(self):
        return u'{0} {1}'.format(self.pk, self.title)

    def get_absolute_url(self):
        return reverse('tasks:by_tag', self.title)
