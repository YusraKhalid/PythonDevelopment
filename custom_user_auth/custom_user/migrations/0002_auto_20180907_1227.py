# Generated by Django 2.1.1 on 2018-09-07 12:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('custom_user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='date_joined',
            field=models.DateTimeField(default='2018-09-07 12:27:47.886916'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='groups',
            field=models.ManyToManyField(to='auth.Group'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='permissions',
            field=models.ManyToManyField(to='auth.Permission'),
        ),
    ]
