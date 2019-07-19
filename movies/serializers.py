import random

from rest_framework import serializers

from accounts.models import LikeDisLikeMarked
from .models import Movie, Genre, MovieContinue


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'horizontal_image_path', 'vertical_image']


class HomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'horizontal_image_path', 'vertical_image']
        # fields = '__all__'
        
    def to_representation(self, instance):
        serializers_data = super().to_representation(instance)
        sub_user_id = self.context['sub_user_id']

        """
        "재생중인 목록, 
        찜 목록, 
        넷플릭스 오리지널, 
        추천 영화, 
        OST좋은것,
        여름과 관련 영화, 
        디즈니 영화, 
        미친듯이 웃을 수 있는 영화, 
        영어공부하기 좋은 영화
        """
        speical_list = ['넷플릭스 오리지널', '추천 영화', 'OST좋은것', '여름과 관련 영화',
                        '디즈니 영화', '미친듯이 웃을 수 있는 영화', '영어공부하기 좋은 영화', ]


class ListByMovieGenreAll(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # fields = ['id', 'name', 'horizontal_image_path', 'vertical_image']
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        serializer_data = super().to_representation(instance)

        # 지정해둔 영화 장르를 넘겨받은 context에서 가져옴
        print(self.context)
        genre_list = self.context['genre_list']
        genre_movie_list = dict()

        # 장르별 영화 목록을 가져와 dict 으로 만듬
        for genre in genre_list:
            if genre == '외국 영화':
                movie_list = Movie.objects.exclude(genre__name__icontains='한국 영화')[:1]
            else:
                movie_list = Movie.objects.filter(genre__name__icontains=genre)[:20]
            movie_list_serializer = MovieSerializer(movie_list, many=True)
            genre_movie_list[genre] = movie_list_serializer.data
        return {'메인 영화': serializer_data, '장르별 영화리스트': genre_movie_list}


class PreviewCellListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'circle_image', 'logo_image_path', 'video_file', 'vertical_sample_video_file', ]


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


class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        depth = 2

    def to_representation(self, instance):
        serializer_data = super().to_representation(instance)

        sub_user_id = self.context['sub_user_id']
        print(sub_user_id)
        if instance.like.filter(sub_user=sub_user_id):
            # 해당 서브유저의 좋아요 정보에 접근해서 찜목록과 좋아요 여부를 확인
            like_dislike_marked = instance.like.filter(sub_user=sub_user_id)[0]
            marked = like_dislike_marked.marked
            like = like_dislike_marked.like_or_dislike
        else:
            marked = False
            like = 0

        # 임시적으로 일치율 설정
        match_rate = random.randint(70, 97)

        # 영화정보의 러닝타임( x시간 x분 형식)과 유저가 이전에 재생을 멈춘시간을 xx분 형식으로 변환해서 남은시간과 총시간을 반환
        runningtime = instance.running_time.split('시간 ')
        total_minute = int(runningtime[0]) * 60 + int(runningtime[1][:-1])

        if instance.movie_continue.filter(sub_user_id=sub_user_id):
            to_be_continue = instance.movie_continue.filter(sub_user_id=sub_user_id)[0].to_be_continue
            time_list = instance.movie_continue.filter(sub_user_id=sub_user_id)[0].to_be_continue.split(':')
            spent_time = int(time_list[0]) * 60 + int(time_list[1])
            remaining_time = total_minute - spent_time
        else:
            to_be_continue = None
            remaining_time = None

        # 저장가능 영화인지 확인
        can_i_store = int(instance.production_date) < 2015

        # 계산한 값들을 반환할 딕셔너리에 추가
        key_list = ['marked', 'like', 'match_rate', 'total_minute', 'to_be_continue', 'remaining_time', 'can_i_store']
        value_list = [marked, like, match_rate, total_minute, to_be_continue, remaining_time, can_i_store]

        for i in range(len(key_list)):
            serializer_data[f'{key_list[i]}'] = value_list[i]

        # 선택된 영화와 같은 장르를 가진 영화 6개를 골라서 딕셔너리에 추가
        genre = instance.genre.all()[0]
        similar_movies = genre.movie.exclude(pk=instance.id)[:6]
        similar_movies_serializer = MovieSerializer(similar_movies, many=True)

        # 골라진 6개의 영화가 서브유저에게 찜되었는지 여부를 확인해서 영화정보 뒤에 추가
        for i in range(len(similar_movies_serializer.data)):
            if similar_movies[i].like.filter(sub_user_id=sub_user_id):
                similar_movies_serializer.data[i]['marked'] = similar_movies[i].like.filter(sub_user_id=sub_user_id)[
                    0].marked
            else:
                similar_movies_serializer.data[i]['marked'] = False

        serializer_data['similar_movies'] = similar_movies_serializer.data
        return serializer_data


class LikeDisLikeMarkedSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDisLikeMarked
        fields = ['movie']
        depth = 2


class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MovieOfMovieContinueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'name', 'video_file', 'logo_image_path', 'horizontal_image_path', 'vertical_image')


class MovieContinueMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'id',
            'name',
        )


class MovieContinueSerializer(serializers.ModelSerializer):
    movie_id = MovieContinueMovieSerializer()

    class Meta:
        model = MovieContinue
        fields = ('movie_id', 'to_be_continue')
