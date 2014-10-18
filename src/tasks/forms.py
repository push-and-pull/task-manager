# coding: utf-8

from tasks.models import Task, Tag
from django import forms


class TaskCreateForm(forms.ModelForm):
    tags = forms.CharField()

    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'due_date', 'tags')

    def clean(self):
        import ipdb
        ipdb.set_trace()
        data_tags = self.cleaned_data['tags']
        tag_list = data_tags.split(',')
        for tag in tag_list:
            tag = tag.strip(' ')
            try:
                tag_object = Tag.objects.get(title=tag)
            except Tag.DoesNotExist:
                tag_object = Tag(title=tag)
                tag_object.save()
        self.save()
