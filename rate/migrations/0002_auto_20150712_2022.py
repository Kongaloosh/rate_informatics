# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='course',
        ),
        migrations.AddField(
            model_name='rating',
            name='course',
            field=models.ForeignKey(default='adfs', to='rate.Course'),
            preserve_default=False,
        ),
    ]
