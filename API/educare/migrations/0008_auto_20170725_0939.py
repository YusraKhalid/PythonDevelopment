# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-25 09:39
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educare', '0007_auto_20170725_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='subjects',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('Math', 'Mathematics'), ('Eng', 'English'), ('Bio', 'Biology'), ('Chem', 'Chemistry'), ('Phy', 'Physics'), ('Acc', 'Accounting'), ('BStd', 'Business Studies'), ('Eco', 'Economics')], default='', max_length=4), default=[], size=8),
        ),
    ]
