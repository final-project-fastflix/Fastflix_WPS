from django.urls import path

from .api_view import *

app_name = 'accounts'

urlpatterns = [
    path('create_user/', UserCreate.as_view(), name='create_user'),
    path('create_sub_user/', SubUserCreate.as_view(), name='create_sub_user'),
    path('login/', Login.as_view(), name='login'),
    path('sub_user_list/', SubUserList.as_view(), name='ret_sub_user'),
    path('change_profile/', ChangeProfileImageList.as_view(), ),
    path('change_sub_user/', SubUserModify.as_view(), name='change_sub_user'),
    path('delete_sub_user/', SubUserDelete.as_view(), name='delete_sub_user'),
    path('visited_base_movies/', VisitedBaseMovies.as_view(), name='visited_base_movies'),
]
