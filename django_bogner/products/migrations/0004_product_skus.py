# Generated by Django 2.2.4 on 2019-08-23 11:58

import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='skus',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True), blank=True, null=True, size=None),
        ),
    ]
