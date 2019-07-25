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
    name = models.CharField(max_length=20, unique=True)
    parent_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sub_user')
    kid = models.BooleanField(default=False, blank=True)
    profile_image_path = models.TextField(blank=True)

    def __str__(self):
        return self.name


class LikeDisLikeMarked(models.Model):
    CHOICES_LIKE_STATUS = (
        ('like', 'Like'),
        ('dislike', 'Dislike'),
        ('none', 'None'),
    )
    movie = models.ForeignKey(Movie, related_name='like', on_delete=models.CASCADE)
    sub_user = models.ForeignKey(SubUser, related_name='like', on_delete=models.CASCADE)

    # 0: 선택안함 1 : 좋아요,  2 : 싫어요
    like_or_dislike = models.SmallIntegerField(default=0)
    # like_status = models.CharField('좋아요 상태', choices=CHOICES_LIKE_STATUS, default='none', max_length=12)
    marked = models.BooleanField(default=False)
    # 추가
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.movie} ' \
            f'{self.sub_user} ' \
            f'{self.like_or_dislike} ' \
            f'{self.marked} ' \
            f'{self.created} ' \
            f'{self.updated}'


class ProfileImage(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    category = models.CharField(max_length=50, null=True)
    image_path = models.TextField(null=True)

    def __str__(self):
        return f'{self.category} - {self.name}'
