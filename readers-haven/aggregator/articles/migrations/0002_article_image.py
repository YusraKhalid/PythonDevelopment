# Generated by Django 2.2.3 on 2019-07-16 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.URLField(default=None, max_length=600),
            preserve_default=False,
        ),
    ]
