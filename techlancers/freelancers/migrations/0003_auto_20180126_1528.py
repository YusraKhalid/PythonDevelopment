# Generated by Django 2.0.1 on 2018-01-26 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancers', '0002_auto_20180126_1526'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='profile',
            name='objective',
            field=models.TextField(),
        ),
    ]
