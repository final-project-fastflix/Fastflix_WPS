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
    kid = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name


class LikeDisLikeMarked(models.Model):
    movie = models.ForeignKey(Movie, related_name='like', on_delete=models.CASCADE)
    sub_user = models.ForeignKey(SubUser, related_name='like', on_delete=models.CASCADE)

    # 0: 선택안함 1 : 좋아요,  2 : 싫어요
    like_or_dislike = models.SmallIntegerField(default=0)
    marked = models.BooleanField(default=False)
    # 추가
    # created = models.DateTimeField(auto_now_add=True, default=0)
    # updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.movie) + " " + str(self.sub_user) + " " + str(self.like_or_dislike) + " " + str(self.marked)
