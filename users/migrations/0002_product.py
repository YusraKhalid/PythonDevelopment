# Generated by Django 2.2.6 on 2019-10-22 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('category', models.CharField(max_length=50)),
                ('sub_category', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
                ('description', models.CharField(max_length=200)),
                ('pub_date', models.DateField()),
                ('image', models.ImageField(upload_to='shop/images')),
            ],
        ),
    ]
