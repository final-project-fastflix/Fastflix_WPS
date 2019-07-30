import re

from django.db.models import Max, Q, F
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import SubUser
from movies.models import Actor
from .serializers import *


# Create your views here.

# 영화 전체 목록 리스트
class MovieList(generics.ListAPIView):
    """
        전체 영화 목록입니다

        ---
            - id : 영화의 고유 ID
            - name : 영화의 이름
            - horizontal_image_path : 영화 가로 이미지 경로
            - vetical_image : 영화 세로 이미지(추후 변경예정)

    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class HomePage(generics.ListAPIView):
    """
        맨처음 홈페이지 화면입니다

        ---
            - 맨처음 나오는 영화는 맨위에 크게 들어갈 영화 입니다.

            헤더에
            - Authorization : Token 토큰 값
            - subuserid : 프로필계정의 ID

            를 입력해 주세요 (subuserid는 언더바(_)가 없습니다)

            맨마지막에 찜 여부인
                marked : true or false 가 있습니다

    """

    serializer_class = HomePageSerializer

    def get_queryset(self):
        # 랜덤하게 영화 1개를 가져오기 위함
        max_id = Movie.objects.all().aggregate(max_id=Max('id'))['max_id']
        while True:
            pk = random.randint(1, max_id)

            # 랜덤으로 선택한 영화 1편
            queryset = Movie.objects.filter(pk=pk)
            if queryset:
                break

        return queryset

    def get_serializer_context(self):
        sub_user_id = self.request.META['HTTP_SUBUSERID']
        context = super().get_serializer_context()
        context['sub_user_id'] = sub_user_id
        return context


# 영화 탭을 누르면 나오는 화면에 필요한 영화들의 목록
class GenreSelectBefore(generics.ListAPIView):
    """

        영화 탭을 누르면 나오는 화면에 데이터를 전달하는 뷰 입니다

       ---

            헤더에
            - Authorization : Token 토큰 값
            - subuserid : 프로필계정의 ID

            를 입력해 주세요 (subuserid는 언더바(_)가 없습니다)

           맨 처음 나오는 영화 1개는 맨위에 크게 등록되는 영화 입니다

           맨마지막에 찜 여부인
               marked : true or false 가 있습니다

    """
    serializer_class = GenreSelectBeforeSerializer

    def get_queryset(self):
        # 랜덤하게 영화 1개를 가져오기 위함
        max_id = Movie.objects.all().aggregate(max_id=Max('id'))['max_id']
        while True:
            pk = random.randint(1, max_id)

            # 랜덤으로 선택한 영화 1편
            queryset = Movie.objects.filter(pk=pk)
            if queryset:
                break

        return queryset

    def get_serializer_context(self):
        sub_user_id = self.request.META['HTTP_SUBUSERID']
        genre_list = ['한국 영화', '외국 영화', '어린이', '가족', '액션', '스릴러', 'SF',
                      '판타지', '범죄', '호러', '다큐멘터리', '로맨스', '코미디', '애니', '오리지널']
        context = super().get_serializer_context()
        context['genre_list'] = genre_list
        context['sub_user_id'] = sub_user_id
        return context


# 앱을 위한 뷰
class PreviewCellList(generics.ListAPIView):
    """
        앱을 위한 프리뷰셀 API입니다

        ---

        ```
            GET 으로 요청 하시면 됩니다

            리턴값 :
            - id : 영화의 고유 ID
            - name : 영화 이름
            - circle_image : 영화의 원형 이미지
            - logo_image_path : 영화의 로고 이미지 path
            - video_file : 영화 파일
            - vertical_sample_video_file : 영화의 세로 샘플 영상
        ```
    """

    serializer_class = PreviewCellListSerializer

    def get_queryset(self):
        queryset = Movie.objects.all().order_by('?')[:10]

        return queryset


# 영화 장르 리스트
class GenreList(generics.ListAPIView):
    """
        영화 장르 리스트입니다

        ---

            헤더에

            - Authorization : Token 토큰 값

            를 입력해 주세요


            - id : 영화 장르 ID
            - name : 영화 장르
    
    """

    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer


# 장르별 영화 리스트를 전체로 뿌려주기
class MovieListFirstGenre(generics.ListAPIView):
    """
        장르별 영화 리스트 입니다


        ---

            - 요청할때 movie/genre/'카테고리 명'/list/로 요청하시면 됩니다
                - Ex) movie/genre/액션/list/
                - Ex) movie/genre/스릴러/list/

                - name : 영화 이름
                - logo_image_path : 로고 이미지의 경로
                - horizontal_image_path : 가로 이미지 경로
                - vertical_image : 세로 이미지(차후 변경 예정)

    """
    serializer_class = MovieListSerializer

    def get_queryset(self):
        if 'kind' in self.kwargs:
            kind = self.kwargs['kind']
        else:
            kind = None
        sub_user_id = self.request.META['HTTP_SUBUSERID']

        queryset = Movie.objects.filter(genre__name__icontains=kind).exclude(like__sub_user_id=sub_user_id,
                                                                             like__like_or_dislike=2).distinct()[:18]

        return queryset


# 해당 유저의 찜 영화 목록
# 유저별 찜목록 영화 리스트
class MarkedList(generics.ListAPIView):
    """
        유저별 찜 목록 영화 리스트 입니다

        ---

            헤더에
            - Authorization : Token 토큰 값
            - subuserid : 프로필계정의 ID

            를 입력해 주세요 (subuserid는 언더바(_)가 없습니다)


            - 요청할때 "/movies/my_list" 로 요청하시면 됩니다

                - Ex) /movies/my_list/

                - id : 영화의 고유 ID 값
                - name : 영화 이름
                - horizontal_image_path : 가로 이미지 경로
                - vertical_image : 세로 이미지(차후 변경 예정)

    """

    serializer_class = MarkedListSerializer

    def get_queryset(self):
        sub_user_id = self.request.META['HTTP_SUBUSERID']
        queryset = Movie.objects.filter(like__sub_user=sub_user_id, like__marked=True)
        return queryset


# 영화 상세정보 뷰
class MovieDetail(generics.RetrieveAPIView):
    """
        영화 디테일 페이지 url 입니다.

        ---

            헤더에

            - Authorization : Token 토큰 값
            - subuserid : 프로필계정의 ID

            를 입력해 주세요 (subuserid는 언더바(_)가 없습니다)




            - 요청할때 "/movie/'영화 ID값'" 으로 요청하시면 됩니다.

                - Ex) /movie/2
                - Ex) /movie/7

                - id : 영화의 고유 ID 값
                - name : 영화 이름
                - video_file : 비디오파일
                - sample_video_file : 샘플 비디오 파일
                - production_date : 영화 개봉 날짜
                - uploaded_date : 영화 등록(업로드) 날짜
                - synopsis : 영화 줄거리
                - running_time : 영화 러닝타임
                - view_count : 영화 조회수
                - logo_image_path : 로고 이미지의 경로
                - horizontal_image_path : 가로 이미지 경로
                - vertical_image : 세로 이미지(차후 변경 예정)
                - circle_image : 원형 이미지(차후 변경예정)
                - degree : 영화 등급 (Ex.청소년 관람불가, 15세 등등)
                - directors : 영화 감독
                - actors : 배우
                - feature : 영화 특징(Ex.흥미진진)
                - author : 각본가
                - genre : 장르
                - marked : 유저가 찜한 영화인
                - like : 유저가 좋아요한 영화인지, 싫어요한 영화인지 (평가안함 = 0 , 좋아요 = 1, 싫어요 = 2)
                - total_minute : 시간을 분으로 환산한 값
                - match_rate : 일치율(현재 70~97 랜덤, 추후 업데이트 예정)
                - to_be_continue : 유저가 재생을 멈춘시간
                - remaining_time : running_time - to_be_continue
                - can_i_store : 저장가능 여부


    """
    queryset = Movie.objects.all()
    serializer_class = MovieDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        sub_user_id = self.request.META['HTTP_SUBUSERID']
        context['sub_user_id'] = sub_user_id
        return context


# 시청중인 목록 뷰
class FollowUpMovies(generics.ListAPIView):
    """
        메인화면에서 보여줄 시청 중인 영화리스트 url 입니다.

        ---
            - 요청할때 /movies/followup/ 으로 요청하시면 됩니다.
            - 헤더에 subuserid : 서브유저 id 값(int)  을 넣어주셔야 합니다.
                - id : 영화의 고유 ID 값
                - name : 영화 이름
                - video_file : 비디오파일
                - logo_image_path : 로고 이미지의 경로
                - horizontal_image_path : 가로 이미지 경로
                - vertical_image : 세로 이미지(차후 변경 예정)
                - real_running_time : 영상의 실제 총 러닝타임
                - to_be_continue : 유저가 재생을 멈춘시간
                - progress_bar : 영상 진행률

    """

    # queryset = Movie.objects.all()
    serializer_class = MovieContinueSerializer

    def get_queryset(self):
        sub_user_id = self.request.META['HTTP_SUBUSERID']
        queryset = MovieContinue.objects.filter(sub_user_id=sub_user_id)
        return queryset.order_by('-updated')

    def get_serializer_context(self):
        context = super().get_serializer_context()
        sub_user_id = self.request.META['HTTP_SUBUSERID']
        context['sub_user_id'] = sub_user_id
        return context


# 장르별 영화 리스트
class MovieListByGenre(APIView):
    """
        영화 페이지에서 장르를 선택하면 보여줄 영화리스트 url 입니다.

        ---
            - 요청할때 /movies/list_by_genre/'genre_key'/ 로 요청하시면 됩니다.

                - Ex) /movies/list_by_genre/액션/
                - Ex) /movies/list_by_genre/외국/

            genre_key 종류

            '한국', '미국', '어린이', '액션', '스릴러', 'sf', '판타지',
            '범죄', '호러', '다큐', '로맨스', '코미디', '애니', '외국',

            - 헤더에 subuserid : 서브유저 id 값(int)  을 넣어주셔야 합니다.

                - id : 영화의 고유 ID 값
                - name : 영화 이름
                - sample_video_file : 미리보기 비디오파일
                - logo_image_path : 로고 이미지의 경로
                - horizontal_image_path : 가로 이미지 경로
                - vertical_image : 세로 이미지
    """

    def get(self, request, format=None, **kwargs):
        vertical_genre = self.kwargs['genre_key']
        sub_user = self.request.META['HTTP_SUBUSERID']

        genre_list = [
            '한국',
            '미국',
            '어린이',
            '액션',
            '스릴러',
            'sf',
            '판타지',
            '범죄',
            '호러',
            '다큐',
            '로맨스',
            '코미디',
            '애니',
            '외국',
        ]

        context = {}
        vertical_q = Q(genre__name__icontains=vertical_genre)

        for genre in genre_list:
            if vertical_genre == genre:
                continue
            else:
                horizontal_q = Q(genre__name__icontains=genre)
                if vertical_genre == '외국':
                    queryset = Movie.objects.exclude(like__sub_user=sub_user, like__like_or_dislike=2) \
                        .exclude(genre__name__icontains='한국').filter(horizontal_q)

                else:
                    if genre == '외국':
                        queryset = Movie.objects.exclude(like__sub_user=sub_user, like__like_or_dislike=2) \
                            .exclude(genre__name__icontains='한국').filter(vertical_q)
                    else:
                        queryset = Movie.objects.exclude(like__sub_user=sub_user, like__like_or_dislike=2) \
                            .filter(vertical_q).filter(horizontal_q)

                if queryset.count() < 3:
                    continue
                serializer_data = MovieListByGenreSerializer(queryset.distinct(), many=True).data
                random.shuffle(serializer_data)
                context[f'{genre}'] = serializer_data

        if vertical_genre == '외국':
            vertical_queryset = Movie.objects.exclude(like__sub_user=1, like__like_or_dislike=2) \
                .exclude(genre__name__icontains='한국').distinct()
        else:
            vertical_queryset = Movie.objects.exclude(like__sub_user=1, like__like_or_dislike=2) \
                .filter(vertical_q).distinct()

        vertical_serializer_data = MovieListByGenreSerializer(vertical_queryset.order_by('?'), many=True).data
        random.shuffle(vertical_serializer_data)
        context[f'{vertical_genre}'] = vertical_serializer_data

        return Response(context)


# 프로필 생성후 좋아하는 영화 3개 선택하기(무작위 50개) -> 성능 개선 필요
class RecommendMovieAfterCreateSubUser(generics.ListAPIView):
    """
        프로필계정 가입후 좋아하는 영화 목록3개 선택하기입니다. 영화 60개를 리턴합니다.

        ---

            너무 느려서 성능 개선이 필수입니다

            header에

                Authorization: Token "토큰값"

            을 넣어주세요

            리턴값:
                [
                    {
                        "id": 영화의 ID,
                        "name": 영화 제목
                        "horizontal_image_path": 영화의 가로 이미지 path
                        "vertical_image": 영화의 세로 이미지 path
                    },
                    ... 이하 59개 동일
                ]

    """

    serializer_class = MovieSerializer

    def get_queryset(self):
        queryset = Movie.objects.all().order_by('?')[:60]

        return queryset


# 좋아요 목록에 추가하기
class AddLike(APIView):
    """
        좋아요 목록에 추가하는 API뷰 입니다

        ---
            Header
                Authorization: Token 토큰값

            Body
                movieid : 영화의 ID
                subuserid : 서브유저의 ID

            를 넣어서 POST로 요청해 주세요


            리턴값
                좋아요 등록 성공 OR 좋아요 취소 성공


    """

    def post(self, request, *args, **kwargs):
        movie_id = request.data.get('movieid')
        sub_user_id = request.data.get('subuserid')

        sub_user = SubUser.objects.get(id=sub_user_id)
        movie = Movie.objects.get(id=movie_id)

        obj, created = LikeDisLikeMarked.objects.update_or_create(
            movie__name=movie.name,
            sub_user__name=sub_user.name,
            defaults={'movie': Movie.objects.get(name=movie.name),
                      'sub_user': SubUser.objects.get(id=sub_user.id),
                      # 'like_or_dislike': 1,
                      # 'marked': False,
                      # 'created': timezone.now(),
                      'updated': timezone.now(),
                      'movie_id': movie_id,
                      'sub_user_id': sub_user_id})

        if obj.like_or_dislike == 1:
            obj.like_or_dislike = 0
            movie.like_count = F('like_count') - 1
            movie.save()
            obj.save()
            return JsonResponse({'response': False}, status=201)

        if created or obj.like_or_dislike != 1:
            obj.like_or_dislike = 1
            movie.like_count = F('like_count') + 1
            movie.save()
            obj.save()
        return JsonResponse({'response': True}, status=201)


# 싫어요 목록에 추가하기
class AddDisLike(APIView):
    """
        싫어 목록에 추가하는 API뷰 입니다

        ---
            Header
                Authorization: Token 토큰값

            Body
                movieid : 영화의 ID
                subuserid : 서브유저의 ID

            를 넣어서 POST로 요청해 주세요


            리턴값
                싫어요 등록 성공 OR 싫어요 취소 성공


    """

    def post(self, request, *args, **kwargs):
        movie_id = request.data.get('movieid')
        sub_user_id = request.data.get('subuserid')

        sub_user = SubUser.objects.get(id=sub_user_id)
        movie = Movie.objects.get(id=movie_id)

        obj, created = LikeDisLikeMarked.objects.update_or_create(
            movie__name=movie.name,
            sub_user__name=sub_user.name,
            defaults={'movie': Movie.objects.get(name=movie.name),
                      'sub_user': SubUser.objects.get(id=sub_user.id),
                      # 'like_or_dislike': 2,
                      # 'marked': False,
                      # 'created': timezone.now(),
                      'updated': timezone.now(),
                      'movie_id': movie_id,
                      'sub_user_id': sub_user_id})

        if obj.like_or_dislike == 2:
            obj.like_or_dislike = 0
            movie.like_count = F('like_count') + 1
            movie.save()
            obj.save()
            return JsonResponse({'response': False}, status=201)

        if created or obj.like_or_dislike != 2:
            obj.like_or_dislike = 2
            movie.like_count = F('like_count') - 1
            movie.save()
            obj.save()
        return JsonResponse({'response': True}, status=201)


# 찜 목록에 추가하기
class MyList(APIView):
    """
        찜 목록에 추가하는 API뷰 입니다

        ---
            Header
                Authorization: Token 토큰값

            Body
                movieid : 영화의 ID
                subuserid : 서브유저의 ID

            를 넣어서 POST로 요청해 주세요


            리턴값
                marked : True (찜 목록에 등록된 상태)
                         False (찜 목록에 등록되지 않은 상태)


    """

    def post(self, request, *args, **kwargs):
        movie_id = request.data.get('movieid')
        sub_user_id = request.data.get('subuserid')

        sub_user = SubUser.objects.get(id=sub_user_id)
        movie = Movie.objects.get(id=movie_id)

        obj, created = LikeDisLikeMarked.objects.update_or_create(
            movie__name=movie.name,
            sub_user__name=sub_user.name,
            defaults={'movie': Movie.objects.get(name=movie.name),
                      'sub_user': SubUser.objects.get(id=sub_user.id),
                      # 'like_or_dislike': 0,
                      # 'marked': True,
                      # 'created': timezone.now(),
                      'updated': timezone.now(),
                      'movie_id': movie_id,
                      'sub_user_id': sub_user_id})

        if created:
            obj.marked = True
            obj.save()

            return JsonResponse({'marked': True}, status=201)

        # 이미 좋아요나 싫어요 표시를 하여 목록에 있음
        else:
            if obj.marked:
                obj.marked = False
                obj.save()

                return JsonResponse({'marked': False}, status=201)
            else:
                obj.marked = True
                obj.save()
                return JsonResponse({'marked': True}, status=201)


# 최신 등록 영화 10개
class BrandNewMovieList(generics.ListAPIView):
    """
            최신 등록 영화 url 입니다.

        ---
            - /movies/brand_new/ 로 요청하시면 됩니다.

            - 헤더에 subuserid : 서브유저 id 값(int)  을 넣어주셔야 합니다.

                - id : 영화의 고유 ID 값
                - name : 영화 이름
                - sample_video_file : 미리보기 비디오파일 경로
                - logo_image_path : 로고 이미지의 경로
                - horizontal_image_path : 가로 이미지 경로
                - vertical_image : 세로 이미지 경로

    """

    serializer_class = MovieListByGenreSerializer

    def get_queryset(self):
        sub_user = self.request.META['HTTP_SUBUSERID']
        queryset = Movie.objects.exclude(like__sub_user=sub_user, like__like_or_dislike=2).order_by('-created')[:10]

        return queryset


# 절찬 스트리밍 중
class BigSizeVideo(generics.RetrieveAPIView):
    """
        절찬 스트리밍중 (동영상 하나) url 입니다.

        ---
            - /movies/big_size_video/ 로 요청하시면 됩니다.

            - 헤더에 subuserid : 서브유저 id 값(int)  을 넣어주셔야 합니다.

                - id : 영화의 고유 ID 값
                - name : 영화 이름
                - video_file : 비디오파일 경로
                - logo_image_path : 로고 이미지의 경로
                - horizontal_image_path : 가로 이미지 경로
                - marked : 내가 찜한 콘텐츠 인지 여부 (True or False)
                - synopsis : 영화 줄거리
                - big_image_path : big size image path
                - degree : {
                        name : 관람등급 텍스트
                        degree_image_path : 관람등급 이미지 경로
                }
    """

    serializer_class = BigSizeVideoSerializer

    def get_object(self):
        movie_id = 354
        obj = Movie.objects.get(pk=movie_id)
        return obj

    def get_serializer_context(self):
        sub_user_id = self.request.META['HTTP_SUBUSERID']
        context = super().get_serializer_context()
        context['sub_user_id'] = sub_user_id
        return context


# 좋아요 상위 10개
class MostLikesMoives(generics.ListAPIView):
    """
            좋아요 상위 10개 영화 url 입니다.

        ---
            - /movies/most_likes/ 로 요청하시면 됩니다.

            - 헤더에 subuserid : 서브유저 id 값(int)  을 넣어주셔야 합니다.

                - id : 영화의 고유 ID 값
                - name : 영화 이름
                - sample_video_file : 미리보기 비디오파일 경로
                - logo_image_path : 로고 이미지의 경로
                - horizontal_image_path : 가로 이미지 경로
                - vertical_image : 세로 이미지 경로

    """

    serializer_class = MovieListByGenreSerializer

    def get_queryset(self):
        sub_user_id = self.request.META['HTTP_SUBUSERID']
        queryset = Movie.objects.exclude(like__sub_user=sub_user_id, like__like_or_dislike=2).order_by(
            '-like_count')[:10]

        return queryset


# 플레이어 재생시간 저장
class SavePausedVideoTime(APIView):
    """
            비디오 재생시간 저장 url 입니다.

        ---
            - /movies/paused_time/ 로 요청하시면 됩니다.

            - body에
                sub_user_id : 서브유저 id (int)
                movie_id    : 저장할 영화 id (int)
                paused_time : 유저가 시청한 초단위 시간 (int)

                을 넣어주셔야 합니다.

                저장에 성공했을 경우
                {'saved' : True} 가 반환됩니다.
    """

    def post(self, *args, **kwargs):
        paused_time = self.request.data.get('paused_time')
        sub_user_id = self.request.data.get('sub_user_id')
        movie_id = self.request.data.get('movie_id')

        movie_obj = Movie.objects.get(pk=movie_id)
        sub_user_obj = SubUser.objects.get(pk=sub_user_id)

        movie = MovieContinue.objects.get_or_create(movie=movie_obj, sub_user=sub_user_obj)[0]
        movie.to_be_continue = paused_time
        movie.save()

        return Response({'saved': True})


class Search(APIView):
    """
        검색 API View 입니다

        ---

        리턴값 :
            contents -> 영화 검색시 최상단에 나오는 '다음과 관련된 콘텐츠'입니다
            first_movie -> 내가 원하는 영화 입니다(*제일먼저 출력해주세요!*)
            other_movie -> 내가 원하는 영화와 관련된 장르의 영화입니다


    """

    def get(self, *agrs, **kwargs):
        search_key = self.request.GET.get('search_key', None)
        print(search_key)
        if search_key:

            # 주어진 문자열에서 문자와 숫자를 제외한 문자(특수문자)를 삭제함
            re_search_key = re.sub(r'[\W]+', '', search_key)

            # 영화이름중 검색어가 포함된 영화 목록
            movies_name = Movie.objects.filter(name__icontains=re_search_key)

            # 영화 장르중 검색어가 포함된 영화 목록
            movie_genre = Movie.objects.prefetch_related('genre').filter(genre__name__icontains=re_search_key)

            # 배우들 중 검색어가 포함된 영화 목록
            movie_actor = Movie.objects.prefetch_related('actors').filter(actors__name__icontains=re_search_key)

            # 검색어로 시작하는 영화(내가 찾고자 하는 영화라고 예상함)를 맨 처음 보여주기 위함
            temp1 = Movie.objects.filter(name__startswith=re_search_key)
            first_show = temp1.union(movie_actor)

            first_movies_serializer = MovieSerializer(first_show, many=True)

            # 내가 찾고자 하는 영화를 보여주고 난뒤 나머지 영화를 보여줌
            queryset = (movies_name | movie_genre | movie_actor).difference(first_show).distinct()

            count = queryset.count()
            # 검색 결과가 60개가 안될경우
            if count <= 59:
                require_count = 60 - count
                if first_show:
                    # 내가 찾고자 하는 영화중에 있으면 그것과 관련된 장르의 영화를 보여줌
                    genre = first_show[0].genre.all()[0].name
                else:
                    # 없다면 임의로 나온 영화중 관련된 장르의 영화를 보여줌
                    genre = queryset[0].genre.all()[0].name
                new_list = Movie.objects.filter(genre__name=genre)[:require_count]
                queryset = queryset.union(new_list).difference(first_show)

            queryset_serializer = MovieSerializer(queryset, many=True)

            # 다음과 관련된 콘텐츠 최대 10개
            # 관련된 영화 이름
            movie_name = first_show[:5]
            # 관련된 장르 이름
            genre_name = Genre.objects.filter(name__icontains=re_search_key)[:5]
            # 관련된 영화배우 이름
            actor_name = Actor.objects.filter(name__startswith=re_search_key)[:5]

            contents = []
            for movie in movie_name:
                contents.append(movie.name)
            for actor in actor_name:
                contents.append(actor.name)
            for genre in genre_name:
                contents.append(genre.name)

            return JsonResponse({'contents': contents,
                                 'first_movie': first_movies_serializer.data,
                                 'other_movie': queryset_serializer.data,
                                 }, status=201)
        else:
            return JsonResponse({'search_error': False}, status=403)


class MatchRate(APIView):
    sub_user_id = 8
    sub_user = SubUser.objects.get(pk=sub_user_id)
    marked_obj = sub_user.like.filter(marked=True)
