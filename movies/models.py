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
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name = models.CharField(max_length=50)

    video_file = models.FileField(upload_to=f'media/movie/{name}/video', blank=True, null=True)
    sample_video_file = models.FileField(upload_to=f'media/movie/{name}/sample_video', blank=True, null=True)

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

    logo_image_path = models.TextField(default=None, blank=True, null=True)
    horizontal_image_path = models.TextField(default=None, blank=True, null=True)
    vertical_image = models.ImageField(upload_to=f'media/movie/{name}/horizontal')
    circle_image = models.ImageField(upload_to=f'media/movie/{name}/circle', null=True, blank=True)
    big_image_path = models.TextField(default=None, null=True, blank=True)

    def __str__(self):
        return self.name


class MovieContinue(models.Model):
    movie_id = models.ForeignKey(Movie, related_name='movie_continue', on_delete=models.CASCADE)
    sub_user_id = models.ForeignKey('accounts.SubUser', related_name='movie_continue', on_delete=models.CASCADE)
    to_be_continue = models.CharField(max_length=20)

    def __str__(self):
        # return '{movie} {sub_user} {to_be_continue}'.format(
        #     movie=str(self.movie_id),
        #     sub_user=str(self.sub_user_id),
        #     to_be_continue=str(self.to_be_continue),
        # )
        return f'{self.movie_id} {self.sub_user_id} {self.to_be_continue}'
        # return str(self.movie_id) + " " + str(self.sub_user_id) + " " + str(self.to_be_continue)

    # 영화 국적 - 완
    # 이미지필드 최소 3개 - 완
    # 세로 영상 - 보류
    # 미리보기 동영상(마우스 오버를 하면 요청을 받아 보내기) - 완
    # 이미지 가로,세로요청을 헤더로 T/F를 넣어 보냄 - ?
    # 영화 이어보기(멈췄던) 시간 - ?
