# Generated by Django 4.2.7 on 2023-11-23 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iplapp', '0002_alter_franchises_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='franchises',
            name='f_logo',
            field=models.ImageField(blank=True, null=True, upload_to='logos'),
        ),
    ]
