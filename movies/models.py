from django.db import models


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
    parent_genre = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_genre')

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
    movie = models.FileField()
    directors = models.ManyToManyField(Director, related_name='movie_directors')
    actors = models.ManyToManyField(Actor, related_name='movie_actors')
    feature = models.ManyToManyField(Feature, related_name='movie_feature')
    degree = models.ForeignKey(Degree, on_delete=models.SET_NULL, related_name='movie_degree', null=True)
    synopsis = models.TextField()

    def __str__(self):
        return self.name
