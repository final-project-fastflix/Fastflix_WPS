from django.urls import path

from movies.views import update_real
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

    # 장르 전체 목록
    path('genre/list/', GenreList.as_view(), name='genre_list'),

    # 장르별 영화 목록
    path('list_by_genre/<genre_key>/', MovieListByGenre.as_view(), name='MovieListByGenre'),

    # 프로필 계정별 찜 목록
    path('my_list/', MarkedList.as_view(), name="preference_list"),

    # 특정 영화의 상세 페이지
    # sub_user_id가 필요한 이유는
    # 프로필 계정당 좋아요, 싫어요, 찜목록, 재생시간을 불러오기 위함
    path('<int:pk>/', MovieDetail.as_view(), name='movie_detail'),

    # 재생 중 목록
    path('followup/', FollowUpMovies.as_view(), name='follow_up_movies'),

    # 프로필계정 생성후 좋아하는 콘텐츠 선택하기
    path('profiles/setup/', RecommendMovieAfterCreateSubUser.as_view(), name='profiles_setup'),

    # 가장 최근에 등록된 영화 리스트
    path('brand_new/', BrandNewMovieList.as_view()),

    # 카테고리별로 영화 요청
    path('genre/<kind>/list/', MovieListFirstGenre.as_view(), name='genre_movie'),

    # 좋아요 추가
    path('like/', AddLike.as_view(), name='like'),

    # 싫어요 추가
    path('dislike/', AddDisLike.as_view(), name='dislike'),

    # 찜목록 추가, 제거
    path('add_delete_my_list/', MyList.as_view(), name='my_list'),

    # 절찬스트리밍 중
    path('big_size_video/', BigSizeVideo.as_view(), name='big_size_video'),

    # 좋아요 가장 많은 영화
    path('most_likes/', MostLikesMoives.as_view(), name='most_likes_movies'),

    # 유저가 일시정지한 비디오시간 저장
    path('paused_time/', SavePausedVideoTime.as_view(), name='paused_time'),

    # 영화 검색기능
    path('search/', Search.as_view(), name='search'),
    path('update/', update_real,),

    # 영화 추천기능
    path('rcd/', RecommendSystem.as_view(), name='rcd'),

]

