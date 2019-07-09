from django.urls import path
from .views import *

app_name = 'movie'

urlpatterns = [
    path('', MovieList.as_view(), name='sdaflist'),
    path('create/', MovieCerate.as_view(), name='create'),
    path('genre/list/', GenreList.as_view(), name='genre_list'),
    path('genre/<str:kind>/list/', ListByMovieGenre.as_view(), name='genre_kind_list'),
]