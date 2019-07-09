from rest_framework import serializers

from .models import Movie, Genre


class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        depth = 1


class MovieCreateSerializer(serializers.ModelSerializer):
    # logo_image = serializers.ImageField(use_url=True)

    class Meta:
        model = Movie
        fields = '__all__'


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

