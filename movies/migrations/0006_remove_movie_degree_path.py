# Generated by Django 2.2.3 on 2019-07-24 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_auto_20190724_1541'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='degree_path',
        ),
    ]
