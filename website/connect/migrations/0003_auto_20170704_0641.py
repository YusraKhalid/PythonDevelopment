# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-04 06:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('connect', '0002_auto_20170704_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='example@gmail.com', max_length=50),
        ),
    ]
