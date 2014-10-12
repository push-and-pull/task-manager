# coding: utf-8

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView

from tasks.models import Task


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class TaskCreate(CreateView, LoginRequiredMixin):
    model = Task
    fields = ('title', 'description', 'status', 'due_date')
    template_name_suffix = '_create_form'

    def get_success_url(self):
        return reverse('tasks:task_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user

        return super(TaskCreate, self).form_valid(form)


class TaskEdit(UpdateView, LoginRequiredMixin):
    model = Task
    fields = ('title', 'description', 'status', 'due_date')
    template_name_suffix = '_create_form'


class TaskList(ListView, LoginRequiredMixin):
    context_object_name = 'task_list'

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user.pk)


class TaskDetail(DetailView, LoginRequiredMixin):
    model = Task
    context_object_name = 'task'
