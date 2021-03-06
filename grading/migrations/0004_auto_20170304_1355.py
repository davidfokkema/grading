# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-04 12:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grading', '0003_auto_20170303_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=40)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='grading.Course')),
            ],
        ),
        migrations.RenameField(
            model_name='student',
            old_name='course',
            new_name='courses',
        ),
    ]
