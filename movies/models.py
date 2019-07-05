from django.db import models
from django.utils import timezone
# Create your models here.


class Director(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Actor(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name


class Feature(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Degree(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=50)
    video_file = models.FileField(upload_to='media/%Y/%m/%d')
    directors = models.ManyToManyField(Director, related_name='movie_directors')
    actors = models.ManyToManyField(Actor, related_name='movie_actors')
    feature = models.ManyToManyField(Feature, related_name='movie_feature')
    author = models.ManyToManyField(Author, related_name='movie_author')
    degree = models.ForeignKey(Degree, on_delete=models.SET_NULL, related_name='movie_degree', null=True)
    genre = models.ManyToManyField(Genre, related_name='movie_genre')
    production = models.DateField(default=timezone.now)
    uploaded = models.DateField(default=timezone.now)
    synopsis = models.TextField()
    running_time = models.CharField(max_length=10)

    def __str__(self):
        return self.name
