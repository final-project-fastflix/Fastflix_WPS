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
    logined = models.BooleanField(default=False, blank=True) # 서버에서 체크하는 대신 클라이언트에서 sub_usr_id를 받기로 함

    def __str__(self):
        return self.name


class LikeDisLikeMarked(models.Model):
    movie = models.ForeignKey(Movie, related_name='like', on_delete=models.CASCADE)
    sub_user = models.ForeignKey(SubUser, related_name='like', on_delete=models.CASCADE)

    # 0: no choice 1 : like,  2 : dislike
    like_or_dislike = models.SmallIntegerField(default=0)
    marked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.movie) + " " + str(self.sub_user) + " " + str(self.like_or_dislike) + " " + str(self.marked)
