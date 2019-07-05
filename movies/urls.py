from django.urls import path
from .views import *

app_name = 'movie'

urlpatterns = [
    path('', MovieList.as_view(), name='list'),
    path('create/', MovieCerate.as_view(), name='create'),
    path('genre/list/', GenreList.as_view(), name='genre_list'),
]