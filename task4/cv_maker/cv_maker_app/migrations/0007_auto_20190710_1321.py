# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-10 13:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cv_maker_app', '0006_auto_20190710_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinformation',
            name='image',
            field=models.FileField(upload_to='documents/'),
        ),
    ]