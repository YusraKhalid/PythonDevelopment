# Generated by Django 2.0.7 on 2018-07-24 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_auto_20180724_0933'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=' ', max_length=50)),
                ('deleted', models.BooleanField(default=False)),
            ],
        ),
    ]
