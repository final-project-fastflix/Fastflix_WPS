from rest_framework import serializers

from .models import Movie, Genre


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        depth = 1



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
