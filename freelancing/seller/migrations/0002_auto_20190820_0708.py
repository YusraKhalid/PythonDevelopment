# Generated by Django 2.2.4 on 2019-08-20 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='delivery_time',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='package',
            name='revisions',
            field=models.IntegerField(),
        ),
    ]