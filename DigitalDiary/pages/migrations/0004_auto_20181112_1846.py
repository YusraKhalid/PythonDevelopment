# Generated by Django 2.1.2 on 2018-11-12 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='creator',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='note',
            name='body',
            field=models.CharField(max_length=500),
        ),
    ]
