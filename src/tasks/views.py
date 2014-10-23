# coding: utf-8

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView, DetailView
from tasks.forms import TaskCreateForm
import ipdb


from tasks.models import Task, Tag


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class TaskCreate(CreateView, LoginRequiredMixin):
    model = Task
    form_class = TaskCreateForm

    template_name_suffix = '_create_form'

    def get_success_url(self):
        return reverse('tasks:task_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        self.object = form.save()
        for tag_title in form.cleaned_data['tag_set']:
            self.object.tag_set.add(Tag.objects.get(title=tag_title))
        self.object.save()
        return super(TaskCreate, self).form_valid(form)


class TaskEdit(UpdateView, LoginRequiredMixin):
    model = Task
    form_class = TaskCreateForm
    template_name_suffix = '_create_form'

    def get_success_url(self):
        return reverse('tasks:task_list')


class TaskList(ListView, LoginRequiredMixin):
    context_object_name = 'task_list'

    ORDER_BY = {
        'due_date': '-due_date',
        'created_at': '-created_at'
    }
    DEFAULT_ORDER = 'pk'

    def get_queryset(self):
        order = self.request.GET.get('order_by')
        order_by = self.ORDER_BY.get(order, self.DEFAULT_ORDER)
        queryset = Task.objects.filter(created_by=self.request.user.pk).order_by(order_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        return context


class TaskListByTag(ListView, LoginRequiredMixin):
    context_object_name = 'task_list'

    ORDER_BY = {
        'due_date': '-due_date',
        'created_at': '-created_at'
    }
    DEFAULT_ORDER = 'pk'

    def get_queryset(self):
        order = self.request.GET.get('order_by')
        order_by = self.ORDER_BY.get(order, self.DEFAULT_ORDER)
        tag = self.kwargs['tag']
        queryset = Task.objects.filter(created_by=self.request.user.pk,
                                       tag=Tag.objects.get(title=tag)).order_by(order_by)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TaskListByTag, self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        return context


class TaskDetail(DetailView, LoginRequiredMixin):
    model = Task
    context_object_name = 'task'
