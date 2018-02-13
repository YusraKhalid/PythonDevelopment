# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-11 06:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('grade', '0002_gradecourse'),
    ]

    operations = [
        migrations.CreateModel(
            name='GradeStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gradestudent_grade', to='grade.Grade')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gradestudent_student', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GradeTeacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gradeteacher_grade', to='grade.Grade')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gradeteacher_teacher', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
