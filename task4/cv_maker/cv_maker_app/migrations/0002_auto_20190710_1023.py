# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-10 10:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cv_maker_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinformation',
            name='email',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='basicinformation',
            name='skill1_level',
            field=models.CharField(choices=[('1', 'Beginner'), ('2', 'Little Knowledge'), ('3', 'Intermediate'), ('4', 'Advance'), ('5', 'Expert')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='basicinformation',
            name='skill2_level',
            field=models.CharField(choices=[('1', 'Beginner'), ('2', 'Little Knowledge'), ('3', 'Intermediate'), ('4', 'Advance'), ('5', 'Expert')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='basicinformation',
            name='skill3_level',
            field=models.CharField(choices=[('1', 'Beginner'), ('2', 'Little Knowledge'), ('3', 'Intermediate'), ('4', 'Advance'), ('5', 'Expert')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='basicinformation',
            name='skill4_level',
            field=models.CharField(choices=[('1', 'Beginner'), ('2', 'Little Knowledge'), ('3', 'Intermediate'), ('4', 'Advance'), ('5', 'Expert')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='basicinformation',
            name='skill5_level',
            field=models.CharField(choices=[('1', 'Beginner'), ('2', 'Little Knowledge'), ('3', 'Intermediate'), ('4', 'Advance'), ('5', 'Expert')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='experience',
            name='ending_date',
            field=models.DateField(null=True),
        ),
    ]