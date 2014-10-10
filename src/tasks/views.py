# coding: utf-8
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView

from tasks.models import Task


class TaskCreate(CreateView):
    model = Task
    fields = ('title', 'description', 'status', 'due_date')
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.created_by = self.request.user

        return super(TaskCreate, self).form_valid(form)


class TaskEdit(UpdateView):
    model = Task
    fields = ('title', 'description', 'status', 'due_date')
    template_name_suffix = '_create_form'


class TaskList(ListView):
    context_object_name = 'task_list'

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user.pk)


class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'
