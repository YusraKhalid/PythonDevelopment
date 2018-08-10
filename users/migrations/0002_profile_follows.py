# Generated by Django 2.0.7 on 2018-08-10 13:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0002_auto_20180730_0910'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='follows',
            field=models.ManyToManyField(blank=True, related_name='profiles', to='comments.Follow'),
        ),
    ]
