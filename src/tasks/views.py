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
        #fixme check if there is self.object before line 34
        self.object = form.save()
        for tag_title in form.cleaned_data['tag_set']:
            try:
                tag_object = Tag.objects.get(title=tag_title)
            except Tag.DoesNotExist:
                tag_object = Tag(title=tag_title)
                tag_object.save()
            self.object.tag_set.add(tag_object)
        self.object.save()
        #fixme check what returns
        return super(TaskCreate, self).form_valid(form)


class TaskEdit(UpdateView, LoginRequiredMixin):
    model = Task
    form_class = TaskCreateForm
    template_name_suffix = '_create_form'

    def get_success_url(self):
        return reverse('tasks:task_list')

    def get_initial(self):
        initial = super(UpdateView, self).get_initial()
        existing_tag_set = self.object.tag_set.all()
        tag_list = list()
        for tag in existing_tag_set:
            tag_list.append(tag.title)
        tag_list.sort()
        initial['tag_set'] = ', '.join(tag_list)
        return initial

    def form_valid(self, form):
        self.object.tag_set.clear()
        for tag_title in form.cleaned_data['tag_set']:
            try:
                tag_object = Tag.objects.get(title=tag_title)
            except Tag.DoesNotExist:
                tag_object = Tag(title=tag_title)
                tag_object.save()
            self.object.tag_set.add(tag_object)
        self.object.save()
        #fixme check what returns
        return super(TaskEdit, self).form_valid(form)


class TaskList(ListView, LoginRequiredMixin):
    context_object_name = 'task_list'

    paginate_by = 10

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
        context['order_by'] = self.request.GET.get('order_by')
        return context


class TaskListByTag(ListView, LoginRequiredMixin):
    context_object_name = 'task_list'
    paginate_by = 10

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
        context['order_by'] = self.request.GET.get('order_by')
        return context


class TaskDetail(DetailView, LoginRequiredMixin):
    model = Task
    context_object_name = 'task'
