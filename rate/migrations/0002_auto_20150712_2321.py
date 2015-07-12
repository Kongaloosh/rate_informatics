# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rate', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='lecturer_2',
            field=models.ForeignKey(related_name='second_lecturer', default=None, to='rate.Lecturer', null=True),
        ),
    ]
