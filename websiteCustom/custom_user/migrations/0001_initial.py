# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 07:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=254, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=254)),
                ('second_name', models.CharField(blank=True, max_length=254)),
                ('email', models.EmailField(blank=True, max_length=254, unique=True)),
                ('address1', models.CharField(blank=True, max_length=254)),
                ('address2', models.CharField(blank=True, max_length=254)),
                ('area_code', models.CharField(blank=True, max_length=20)),
                ('country_code', models.CharField(blank=True, max_length=10)),
                ('date_joined', models.DateTimeField(default=datetime.datetime(2017, 6, 30, 7, 59, 12, 54962, tzinfo=utc))),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
    ]
