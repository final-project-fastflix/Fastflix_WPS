from django.urls import path

from accounts.views import upload_images, add_f_category
from .api_view import *

app_name = 'accounts'

urlpatterns = [
    path('create_user/', UserCreate.as_view(), name='create_user'),
    path('create_sub_user/', SubUserCreate.as_view(), name='create_sub_user'),
    path('login/', Login.as_view(), name='login'),
    # path('like_or_dislike/<int:sub_user_id>/<int:movie_id>/', LikeOrDislike.as_view(), name='like_or_dislike'),
    path('sub_user_list/', SubUserList.as_view(), name='ret_sub_user'),
    path('change_profile/', ChangeProfileImageList.as_view(), ),
    path('add/', add_f_category,),
]
