# Generated by Django 2.1 on 2018-08-15 09:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20180815_0733'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='pair_id',
            new_name='pair',
        ),
    ]