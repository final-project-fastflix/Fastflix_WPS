from django.shortcuts import render
from django.views import View
from rest_framework import generics
from .serializers import *
from .models import *
# Create your views here.


class MovieList(generics.ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer


class MovieCerate(generics.CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieCreateSerializer


class GenreList(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreListSerializer


class CreateLike(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if 'movie_id' in kwargs['movie_id']:
                parent_user = request.user
                sub_user = parent_user.sub_user.all().filter(logined=True)
                movie = Movie.objects.get(pk=request.kwargs['movie_id'])
                if sub_user in movie.likes.all():
                    movie.like.remove(sub_user)
                else:
                    movie.like.add(sub_user)