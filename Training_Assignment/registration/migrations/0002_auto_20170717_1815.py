# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 13:15
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, default='+9999999999', max_length=15, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+9999999999'.", regex='^\\+?\\d{10,15}$')]),
        ),
    ]
