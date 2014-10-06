# coding: utf-8
from django.views.generic.edit import CreateView

from tasks.models import Task


class TaskCreate(CreateView):
    model = Task
    fields = ('title', 'description', 'status', 'due_date')
    template_name_suffix = '_create_form'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        import ipdb; ipdb.set_trace()

        return super(TaskCreate, self).form_valid(form)
