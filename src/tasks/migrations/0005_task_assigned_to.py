# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('tasks', '0004_auto_20141104_1025'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='assigned_to',
            field=models.ForeignKey(related_name=b'assigned_to', verbose_name=b'Assigned to', to='users.User', null=True),
            preserve_default=True,
        ),
    ]
