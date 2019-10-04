# Generated by Django 2.2.4 on 2019-10-04 06:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_transaction', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=100)),
                ('cart', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='payment', to='users.Cart')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
