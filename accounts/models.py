# Create your models here.
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

from django.db import models
from movies.models import Movie


class User(AbstractUser):
    birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username


class SubUser(models.Model):

    name = models.CharField(max_length=20)
    parent_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sub_user')
    like = models.ManyToManyField(Movie, related_name='likes')
    # dislike = models.ManyToManyField(Movie, related_name='dislikes')
    kid = models.BooleanField(default=False)
    logined = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class DisLike(models.Model):
    movie = models.ForeignKey(Movie, related_name='dislike', on_delete=models.CASCADE)
    sub_user = models.ForeignKey(SubUser, related_name='dislike', on_delete=models.CASCADE)
