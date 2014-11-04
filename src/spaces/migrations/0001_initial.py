# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('tasks', '0004_auto_20141102_1737'),
    ]

    operations = [
        migrations.CreateModel(
            name='Space',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('created_by', models.ForeignKey(related_name=b'space_created_by', verbose_name=b'Created by', to='users.User')),
                ('tasks', models.ManyToManyField(to='tasks.Task')),
                ('users', models.ManyToManyField(related_name=b'users', to='users.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
