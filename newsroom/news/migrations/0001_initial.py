# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 15:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField()),
                ('published_date', models.DateField()),
                ('scraped_date', models.DateField(auto_now_add=True)),
                ('source_url', models.URLField(unique=True)),
                ('image_url', models.URLField()),
                ('abstract', models.TextField()),
                ('detail', models.TextField()),
                ('summary', models.TextField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Category')),
            ],
            options={
                'verbose_name_plural': 'News',
            },
        ),
        migrations.CreateModel(
            name='Newspaper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('source_url', models.URLField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewsSource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Scrapper',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('newspaper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Newspaper')),
            ],
        ),
        migrations.AddField(
            model_name='news',
            name='news_source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.NewsSource'),
        ),
        migrations.AddField(
            model_name='news',
            name='newspaper',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='news.Newspaper'),
        ),
    ]
