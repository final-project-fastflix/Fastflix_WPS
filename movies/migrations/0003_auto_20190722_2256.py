# Generated by Django 2.2.3 on 2019-07-22 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_movie_vertical_sample_video_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='degree',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
