# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-03 15:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grading', '0002_auto_20170301_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='title',
            field=models.CharField(max_length=80),
        ),
    ]
