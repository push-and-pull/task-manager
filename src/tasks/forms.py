# coding: utf-8

from tasks.models import Task, Tag
from django import forms


class TaskCreateForm(forms.ModelForm):
    tag_set = forms.CharField()

    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'due_date', 'tag_set')

    def clean_tag_set(self):
        tag_list = self.cleaned_data['tag_set'].split(',')
        result = list()
        for tag_title in tag_list:
            tag_title = tag_title.strip(' ')
            result.append(tag_title)
        return result
