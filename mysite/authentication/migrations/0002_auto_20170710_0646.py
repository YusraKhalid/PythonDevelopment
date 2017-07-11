# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 06:46
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 10, 6, 46, 4, 6535, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 10, 6, 46, 4, 6506, tzinfo=utc)),
        ),
    ]
