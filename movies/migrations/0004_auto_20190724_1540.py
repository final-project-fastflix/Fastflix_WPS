# Generated by Django 2.2.3 on 2019-07-24 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_genre_degree_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genre',
            name='degree_path',
        ),
        migrations.AddField(
            model_name='degree',
            name='degree_path',
            field=models.TextField(blank=True),
        ),
    ]
