from django.urls import path

from .api_view import *
from .views import LikeOrDislike, save_data1

app_name = 'accounts'

urlpatterns = [
    path('create_user/', UserCreate.as_view(), name='create_user'),
    path('create_sub_user/', SubUserCreate.as_view(), name='create_sub_user'),
    path('login/', Login.as_view(), name='login'),
    path('like_or_dislike/<int:sub_user_id>/<int:movie_id>/', LikeOrDislike.as_view(), name='like_or_dislike'),
    path('save/', save_data1)
]
