# Generated by Django 2.2.3 on 2019-07-17 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cv_maker_app', '0010_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='skill1',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='skill2',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='skill3',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
