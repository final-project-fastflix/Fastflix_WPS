from django.http import JsonResponse
from django.views import View
from rest_framework import generics
from rest_framework.response import Response

from accounts.models import SubUser
from .serializers import *


# Create your views here.


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


class GenreList(generics.ListAPIView):
    """
        영화 장르 리스트입니다

        ---
            - id : 영화 장르 ID
            - name : 영화 장르
    
    """

    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer


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
    serializer_class = MovieSerializer

    def list(self, request, *args, **kwargs):
        if 'kind' in kwargs:
            kind = kwargs['kind']
        else:
            kind = None

        queryset = Movie.objects.filter(genre__name__icontains=kind).distinct()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


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
    serializer_class = MovieSerializer

    def list(self, request, *args, **kwargs):
        if 'sub_user_id' in kwargs:
            sub_user_id = kwargs['sub_user_id']
        else:
            sub_user_id = None

        queryset = SubUser.objects.get(pk=sub_user_id).like.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        response_list = serializer.data
        print(response_list)
        return Response(response_list)


class MovieDetail(generics.RetrieveAPIView):
    queryset = Movie.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        genre = serializer.data['genre'][0]['name']

        response_list = serializer.data

        movie_list = Movie.objects.filter(genre__name=genre)[:6]
        print(movie_list)
        context = self.get_serializer(movie_list, many=True)
        # print(context.data)

        # response_list.update(context)
        return Response(response_list)

    serializer_class = MovieSerializer


class CreateLike(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if 'movie_id' in kwargs['movie_id']:
                parent_user = request.user
                sub_user = parent_user.sub_user.all().filter(logined=True).get()
                movie = Movie.objects.get(pk=kwargs['movie_id'])
                if sub_user in movie.likes.all():
                    movie.likes.remove(sub_user)
                    return JsonResponse({'data': 'remove'})
                else:
                    movie.likes.add(sub_user)
                    return JsonResponse({'data': 'add'})
