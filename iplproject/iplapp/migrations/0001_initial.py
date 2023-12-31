# Generated by Django 4.2.7 on 2023-11-23 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Franchises',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=30)),
                ('f_nickname', models.CharField(max_length=4)),
                ('f_started_year', models.IntegerField()),
                ('f_logo', models.ImageField(upload_to='logos')),
                ('no_of_trophies', models.IntegerField()),
            ],
        ),
    ]
