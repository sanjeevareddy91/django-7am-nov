# Generated by Django 4.2.7 on 2023-12-14 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iplapp', '0005_userinfo_otp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team1', models.CharField(max_length=4)),
                ('team2', models.CharField(max_length=4)),
                ('winner', models.CharField(max_length=4)),
            ],
        ),
    ]
