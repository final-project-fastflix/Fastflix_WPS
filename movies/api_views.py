from django.db.models import Max
from rest_framework import generics
from rest_framework.response import Response

from accounts.models import SubUser
from .serializers import *


# Create your views here.

# 영화 전체 목록 리스트
class MovieList(generics.ListAPIView):
    """
        전체 영화 목록입니다

        ---
            - id : 영화의 고유 ID
            - name : 영화의 이름
            - video_file : 영화 파일
            - sample_video_file : 영화 샘플 파일
            - production_date : 영화 개봉 날짜
            - uploaded_date : 영화 등록(업로드) 날짜
            - synopsis : 영화 줄거리
            - running_time : 영화 러닝타임
            - view_count : 영화 조회수
            - logo_image_path : 영화 로고 이미지 경로
            - horizontal_image_path : 영화 가로 이미지 경로
            - vetical_image : 영화 세로 이미지(추후 변경예정)
            - circle_image : 영화 동그라미 이미지(추후 변경예정)
            - degree : 영화 등급 (Ex.청소년 관람불가, 15세 등등)
            - directors : 영화 감독
            - actors : 배우
            - feature : 영화 특징(Ex.흥미진진)
            - author : 각본가
            - genre : 장르
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


# 홈페이지 메인에 쓰일 영화 1개
class HomePage(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer

    def list(self, request, *args, **kwargs):
        # 랜덤하게 영화 1개를 가져오기 위함
        max_id = Movie.objects.all().aggregate(max_id=Max('id'))['max_id']
        while True:
            pk = random.randint(1, max_id)

            # 랜덤으로 선택한 영화 1편
            main_movie = Movie.objects.filter(pk=pk).first()
            if main_movie:
                break

        main_movie_serialize = self.get_serializer(main_movie)
        response_list = [main_movie_serialize.data]

        # 전체 영화 장르를 가져옴
        genre_list = Genre.objects.all()

        # 장르별 영화 목록을 가져와 dict 으로 만듬

        for genre in genre_list:
            list_by_genre = Movie.objects.filter(genre__name=genre)
            list_by_genre_serialize = self.get_serializer(list_by_genre, many=True)
            context = list_by_genre_serialize.data
            response_list.append({str(genre): context})

        return Response(response_list)


# 영화 등록
class MovieCerate(generics.CreateAPIView):
    """
        영화 등록 API 입니다

        ---
            - name : 영화 이름
            - production_date : 영화 개봉 날짜
            - uploaded_date : 영화 등록(업로드) 날짜
            - synopsis : 영화 줄거리
            - running_time : 영화 러닝타임
            - view_count : 영화 조회수
            - logo_image_path : 영화 로고 이미지 경로
            - horizontal_image_path : 영화 가로 이미지 경로
            - degree : 영화 등급 (Ex.청소년 관람불가, 15세 등등)
            - directors : 영화 감독
            - actors : 배우
            - feature : 영화 특징(Ex.흥미진진)
            - author : 각본가
            - genre : 장르

    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


# 영화 장르 리스트
class GenreList(generics.ListAPIView):
    """
        영화 장르 리스트입니다

        ---
            - id : 영화 장르 ID
            - name : 영화 장르
    
    """

    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer


# 장르별 영화 리스트
class ListByMovieGenre(generics.ListAPIView):
    """
        장르별 영화 리스트 입니다


        ---

            - 요청할때 movie/genre/'카테고리 명'/list/로 요청하시면 됩니다
                - Ex) movie/genre/액션/list/
                - Ex) movie/genre/스릴러/list/

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

    """

    queryset = Movie.objects.all()
    serializer_class = ListByMovieGenre

    def get_queryset(self):
        if 'kind' in self.kwargs:
            kind = self.kwargs['kind']
        else:
            kind = None

        queryset = Movie.objects.filter(genre__name__icontains=kind).distinct()[:5]

        return queryset


# 해당 유저의 찜 영화 목록
class MarkedList(generics.ListAPIView):
    """
        유저별 찜 목록 영화 리스트 입니다

        ---
            - 요청할때 "/movie/'프로필의 고유 ID값/list/" 로 요청하시면 됩니다

                - Ex) /movie/2/list/
                - Ex) /movie/7/list/

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
    """

    queryset = SubUser.objects.all()
    serializer_class = LikeDisLikeMarkedSerializer

    def list(self, request, *args, **kwargs):
        if 'sub_user_id' in kwargs:
            sub_user_id = kwargs['sub_user_id']
        else:
            sub_user_id = None

        sub_user = SubUser.objects.get(pk=sub_user_id)
        queryset = sub_user.dislike.filter(sub_user=sub_user_id, marked=True)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class MovieDetail(generics.RetrieveAPIView):
    """
        영화 디테일 페이지 url 입니다.

        ---
            - 요청할때 "/movie/'영화 ID값'/'sub_user_id 값'" 으로 요청하시면 됩니다.

                - Ex) /movie/2/1
                - Ex) /movie/7/35

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
        context['sub_user_id'] = self.kwargs['sub_user_id']
        return context

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, *args, **kwargs):
    #     # 영화 오브젝트
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     serializer_data = serializer.data
    #
    #     sub_user_id = kwargs['sub_user_id']
    #     return Response(serializer_data)


class FollowUpMovies(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieContinueSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        sub_user_id = 1
        # queryset = MovieContinue.objects.filter(sub_user_id=sub_user_id)
        queryset = MovieContinue.objects.filter(sub_user_id=sub_user_id)

        # serializer = MovieContinueSerializer(queryset, many=True)
        serializer = self.get_serializer(queryset, many=True)

        # movie_id = queryset[0].movie_id.id
        # print(movie_id)
        # movie = Movie.objects.filter(id=movie_id)
        # print(movie)
        #
        # serializer2 = self.get_serializer(movie, many=True)
        # print(serializer2.data)
        #
        # new_dict = dict()
        # new_dict.update({'1': serializer2.data})
        # print(serializer.data)
        # print(new_dict['1'][0])
        # new_dict['1'][0].update(serializer.data[0])
        # print(new_dict)

        # print(serializer.data)
        return Response(serializer.data)
