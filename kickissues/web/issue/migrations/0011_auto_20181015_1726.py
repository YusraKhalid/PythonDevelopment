# Generated by Django 2.1.2 on 2018-10-15 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0010_auto_20181015_1713'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='assigned_date',
            new_name='assigned_at',
        ),
        migrations.RenameField(
            model_name='issue',
            old_name='resolved_date',
            new_name='resolved_at',
        ),
    ]
