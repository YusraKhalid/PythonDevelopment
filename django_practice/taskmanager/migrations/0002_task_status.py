# Generated by Django 2.2.3 on 2019-08-20 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('complete', 'Complete')], default='Pending', max_length=10),
        ),
    ]