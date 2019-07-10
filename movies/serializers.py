from rest_framework import serializers

from .models import Movie, Genre
from accounts.models import SubUser


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        depth = 1


class MovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class ListByMovieGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        depth = 2


class PreferenceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        depth = 2
