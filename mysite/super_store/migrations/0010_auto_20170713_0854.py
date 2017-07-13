# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-13 08:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('super_store', '0009_brand_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='brands', to=settings.AUTH_USER_MODEL),
        ),
    ]
