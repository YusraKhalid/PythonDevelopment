# Generated by Django 2.1.1 on 2018-09-26 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0002_auto_20180925_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='status',
            field=models.CharField(default='TODO', max_length=20),
        ),
    ]
