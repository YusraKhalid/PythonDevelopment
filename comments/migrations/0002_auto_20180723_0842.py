# Generated by Django 2.2.dev20180707212002 on 2018-07-23 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='articles.Article'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='teams.Player'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='teams.Team'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='article',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='articles.Article'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='player',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='teams.Player'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='teams.Team'),
        ),
    ]
