# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 07:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0009_auto_20170809_0717'),
    ]

    operations = [
        migrations.AddField(
            model_name='appraisal',
            name='description',
            field=models.TextField(default=''),
        ),
    ]
