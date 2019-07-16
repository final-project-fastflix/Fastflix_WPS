from rest_framework import serializers

from .models import Movie, Genre
from accounts.models import LikeDisLikeMarked


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        depth = 2


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'name',
            'sample_video_file',
            'degree',
            'feature',
            'running_time',
            'like',
        ]
        depth = 1


class LikeDisLikeMarkedSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDisLikeMarked
        fields = ['movie']
        depth = 2


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


# class MovieListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = '__all__'
#         depth = 1
#
#
# class MovieCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = '__all__'
#
#
# class ListByMovieGenreSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = '__all__'
#         depth = 2
#
#
# class MarkedListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = '__all__'
#         depth = 2
#
#
# class MovieRetrieve(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = '__all__'
#         depth = 2
