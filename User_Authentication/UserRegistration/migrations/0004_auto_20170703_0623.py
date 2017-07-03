# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-03 06:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserRegistration', '0003_auto_20170630_0858'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='height_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, height_field='height_field', upload_to='profile_picture', width_field='width_field'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='width_field',
            field=models.IntegerField(default=0),
        ),
    ]
