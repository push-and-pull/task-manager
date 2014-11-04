# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spaces', '__first__'),
        ('tasks', '0003_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='space',
            field=models.ForeignKey(verbose_name=b'space', blank=True, to='spaces.Space', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='created_by',
            field=models.ForeignKey(related_name=b'created_by', verbose_name=b'Created by', to='users.User'),
        ),
    ]
