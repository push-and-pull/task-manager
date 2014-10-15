# coding: utf-8

from django.views.generic import ListView
from django.shortcuts import get_object_or_404

from tasks.models import Task
from tags.models import Tag
from tasks.views import LoginRequiredMixin


class TaskListByTag(ListView):
    context_object_name = 'tag'

    ORDER_BY = {
        'due_date': '-due_date',
        'created_at': '-created_at'
    }
    DEFAULT_ORDER = 'title'

    def get_queryset(self):
        order = self.request.GET.get('order_by')
        order_by = self.ORDER_BY.get(order, self.DEFAULT_ORDER)
        self.tag = get_object_or_404(Tag, title=self.args[0])
        queryset = Task.objects.filter(created_by=self.request.user.pk, tag_set=self.tag).order_by(order_by)
        return queryset