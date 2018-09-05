# Generated by Django 2.1 on 2018-08-10 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cnic_no', models.CharField(max_length=16)),
                ('address', models.CharField(max_length=500)),
                ('country', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('postal_code', models.CharField(max_length=10)),
                ('phone_no', models.CharField(max_length=15)),
                ('role', models.CharField(choices=[('DN', 'Donor'), ('CN', 'Consumer')], max_length=2)),
                ('categories', models.ManyToManyField(to='accounts.Category')),
                ('pairId', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Profile', to='accounts.UserProfile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]