# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-06 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grading', '0006_assignment_assignment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='mark',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
