# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, verbose_name=b'Title')),
                ('description', models.TextField(verbose_name=b'Description', blank=True)),
                ('status', models.IntegerField(choices=[(0, b'open'), (1, b'resolved')])),
                ('created_at', models.DateTimeField()),
                ('due_date', models.DateTimeField()),
                ('created_by', models.ForeignKey(verbose_name=b'Created by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
