from django.urls import path
from .api_views import *

app_name = 'movie'

urlpatterns = [
    # 홈페이지 
    path('', HomePage.as_view(), name='home_page'),

    # 전체 목록 중 영화를 눌렀을 경우
    path('genre_select_before/', GenreSelectBefore.as_view(), name='genre_select_before'),

    # 앱을 위한 미리보기 뷰
    path('preview/', PreviewCellList.as_view(), name='preview'),

    # 전체 영화 목록
    path('all/', MovieList.as_view(), name='movie_all_list'),

    # 영화 등록 API
    # path('create/', MovieCerate.as_view(), name='create'),

    # 장르 전체 목록
    path('genre/list/', GenreList.as_view(), name='genre_list'),

    # 장르별 영화 목록
    path('list_by_genre/<genre_key>/<int:sub_user_id>/', MovieListByGenre.as_view(), name='MovieListByGenre'),

    # 프로필 계정별 찜 목록
    path('my_list/', MarkedList.as_view(), name="preference_list"),

    # 특정 영화의 상세 페이지
    # sub_user_id가 필요한 이유는
    # 프로필 계정당 좋아요, 싫어요, 찜목록, 재생시간을 불러오기 위함
    path('<int:pk>/', MovieDetail.as_view(), name='movie_detail'),

    # 재생 중 목록
    path('list_by_genre/<genre_key>/<int:sub_user_id>/', MovieListByGenre.as_view(), name='MovieListByGenre'),
    path('followup/', FollowUpMovies.as_view(), name='follow_up_movies'),
]

