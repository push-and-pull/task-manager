# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('tasks', '0003_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assigned_to',
            field=models.ForeignKey(related_name=b'assigned_to', default=models.ForeignKey(related_name=b'created_by', verbose_name=b'Created by', to='users.User'), verbose_name=b'Assigned to', to='users.User'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='created_by',
            field=models.ForeignKey(related_name=b'created_by', verbose_name=b'Created by', to='users.User'),
        ),
    ]
