# Generated by Django 2.2.4 on 2019-08-29 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsedCars',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=25)),
                ('carmodel', models.CharField(max_length=25)),
                ('year', models.CharField(max_length=10)),
                ('millage', models.CharField(max_length=20)),
                ('transmission', models.CharField(max_length=50)),
                ('engine_type', models.CharField(max_length=50)),
                ('reg_city', models.CharField(max_length=50)),
                ('assembly', models.CharField(max_length=10)),
                ('engine_capacity', models.CharField(max_length=20)),
                ('body_type', models.CharField(max_length=20)),
                ('features', models.TextField()),
                ('description', models.TextField()),
                ('image', models.TextField()),
            ],
        ),
    ]