# coding: utf-8

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView, View

from tasks.models import Task


class LoginRequiredMixin(View):

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

    ORDER_BY = {
        'due_date': '-due_date',
        'created_at': '-created_at'
    }
    DEFALT_ORDER = 'pk'

    def get_queryset(self):
        order = self.request.GET.get('order_by')
        order_by = self.ORDER_BY.get(order, self.DEFALT_ORDER)
        queryset = Task.objects.filter(created_by=self.request.user.pk).order_by(order_by)
        return queryset


class TaskDetail(DetailView, LoginRequiredMixin):
    model = Task
    context_object_name = 'task'
