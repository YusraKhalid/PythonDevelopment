# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-10 10:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cv_maker_app', '0003_auto_20190710_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinformation',
            name='date_of_birth',
            field=models.DateField(),
        ),
    ]