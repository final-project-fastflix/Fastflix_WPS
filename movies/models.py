# Create your models here.
from django.db import models
from django.utils import timezone


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
    name = models.CharField(max_length=30)
    degree_image_path = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=50)

    video_file = models.CharField(max_length=100, blank=True, null=True)
    sample_video_file = models.FileField(upload_to=f'media/movie/{name}/sample_video', blank=True, null=True)
    vertical_sample_video_file = models.FileField(upload_to=f'media/movie/{name}/sample_video', blank=True, null=True)

    directors = models.ManyToManyField(Director, related_name='movie')
    actors = models.ManyToManyField(Actor, related_name='movie')
    feature = models.ManyToManyField(Feature, related_name='movie')
    author = models.ManyToManyField(Author, related_name='movie', blank=True)
    degree = models.ForeignKey(Degree, on_delete=models.SET_NULL, related_name='movie_degree', null=True)
    genre = models.ManyToManyField(Genre, related_name='movie')

    production_date = models.CharField(max_length=10, blank=True)
    uploaded_date = models.DateField(default=timezone.now)

    synopsis = models.TextField(blank=True)
    running_time = models.CharField(max_length=10)
    view_count = models.PositiveIntegerField(default=0)
    like_count = models.IntegerField(default=0)

    logo_image_path = models.TextField(default=None, blank=True, null=True)
    horizontal_image_path = models.TextField(default=None, blank=True, null=True)
    vertical_image = models.TextField(default=None, blank=True, null=True)
    circle_image = models.ImageField(upload_to=f'media/movie/{name}/circle', null=True, blank=True)
    big_image_path = models.TextField(default=None, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class MovieContinue(models.Model):
    movie = models.ForeignKey(Movie, related_name='movie_continue', on_delete=models.CASCADE)
    sub_user = models.ForeignKey('accounts.SubUser', related_name='movie_continue', on_delete=models.CASCADE)
    to_be_continue = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f'{self.movie} {self.sub_user} {self.to_be_continue}'

