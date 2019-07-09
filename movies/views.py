from django.http import JsonResponse
from django.views import View
from rest_framework import generics

from .models import *
from .serializers import *


# Create your views here.


class MovieList(generics.ListAPIView):
    """
        # 전체 영화 목록입니다
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
            - logo_image : 영화 로고 이미지
            - horizontal_image : 영화 가로 이미지
            - vetical_image : 영화 세로 이미지
            - circle_image : 영화 동그라미 이미지
            - degree : 영화 등급 (Ex.청소년 관람불가, 15세 등등)
            - directors : 영화 감독
            - actors : 배우
            - feature : 영화 특징(Ex.흥미진진)
            - author : 각본가
            - genre : 장르
    """
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer


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
            - degree : 영화 등급 (Ex.청소년 관람불가, 15세 등등)
            - directors : 영화 감독
            - actors : 배우
            - feature : 영화 특징(Ex.흥미진진)
            - author : 각본가
            - genre : 장르

    """
    queryset = Movie.objects.all()
    serializer_class = MovieCreateSerializer


class GenreList(generics.ListAPIView):
    """
        영화 장르 리스트입니다
        - id : 영화 장르 ID
        - name : 영화 장르
    
    """
    
    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer


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