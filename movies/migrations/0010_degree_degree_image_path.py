# Generated by Django 2.2.3 on 2019-07-24 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0009_movie_degree_path'),
    ]

    operations = [
        migrations.AddField(
            model_name='degree',
            name='degree_image_path',
            field=models.TextField(blank=True),
        ),
    ]
