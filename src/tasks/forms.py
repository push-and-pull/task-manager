# coding: utf-8

from tasks.models import Task, Tag
from django import forms


class TaskCreateForm(forms.ModelForm):
    tags = forms.CharField()

    class Meta:
        model = Task
        fields = ('title', 'description', 'status', 'due_date', 'tags')

    def clean_tags(self):
        tag_list = self.cleaned_data['tags'].split(',')
        result = list()
        for tag_title in tag_list:
            tag_title = tag_title.strip(' ')
            try:
                Tag.objects.get(title=tag_title)
            except Tag.DoesNotExist:
                tag_object = Tag(title=tag_title)
                tag_object.save()
            result.append(tag_title)
        return result

