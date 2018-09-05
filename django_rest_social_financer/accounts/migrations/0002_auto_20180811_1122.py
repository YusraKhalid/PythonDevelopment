# Generated by Django 2.1 on 2018-08-11 11:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='longitude',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='pairId',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Profile', to='accounts.UserProfile'),
        ),
    ]