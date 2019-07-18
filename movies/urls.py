from django.urls import path
from .api_views import *

app_name = 'movie'

urlpatterns = [
    # 홈페이지 
    path('', HomePage.as_view(), name='home_page'),
    # 전체 목록 중 영화를 눌렀을 경우
    path('genre_select_before/', GenreSelectBefore.as_view(), name='genre_select_before'),
    # 전체 영화 목록
    path('all/', MovieList.as_view(), name='movie_all_list'),
    # 영화 등록 API
    path('create/', MovieCerate.as_view(), name='create'),
    # 장르 전체 목록
    path('genre/list/', GenreList.as_view(), name='genre_list'),
    # 장르별 영화 목록
    path('genre/<str:kind>/list/', ListByMovieGenre.as_view(), name='genre_kind_list'),
    # 프로필 계정별 찜 목록
    path('<int:sub_user_id>/list/', MarkedList.as_view(), name="preference_list"),
    # 특정 영화의 상세 페이지
    # sub_user_id가 필요한 이유는
    # 프로필 계정당 찜목록을 불러오기 위함
    path('<int:pk>/<int:sub_user_id>/', MovieDetail.as_view(), name='movie_detail'),
    # 재생 중 목록
    path('followup/<int:sub_user_id>/', FollowUpMovies.as_view(), name='follow_up_movies'),
]

