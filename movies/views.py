from django.http import JsonResponse
from django.views import View
from rest_framework import generics

from .models import *
from .serializers import *


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
                sub_user = parent_user.sub_user.all().filter(logined=True).get()
                movie = Movie.objects.get(pk=kwargs['movie_id'])
                if sub_user in movie.likes.all():
                    movie.likes.remove(sub_user)
                    return JsonResponse({'data': 'remove'})
                else:
                    movie.likes.add(sub_user)
                    return JsonResponse({'data': 'add'})