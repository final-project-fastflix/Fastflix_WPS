from django.urls import path
from .views import *

app_name = 'movie'

urlpatterns = [
    path('', HomePage.as_view(), name='home_page'),
    path('all/', MovieList.as_view(), name='movie_all_list'),
    path('create/', MovieCerate.as_view(), name='create'),
    path('genre/list/', GenreList.as_view(), name='genre_list'),
    path('genre/<str:kind>/list/', ListByMovieGenre.as_view(), name='genre_kind_list'),
    path('<int:sub_user_id>/list/', MarkedList.as_view(), name="preference_list"),
    path('<int:pk>/', MovieDetail.as_view(), name='movie_detail'),
    # path('save_data/', save_data1,),
]