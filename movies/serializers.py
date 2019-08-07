import random

from rest_framework import serializers

from accounts.models import LikeDisLikeMarked, SubUser
from .models import Movie, Genre, MovieContinue

sub_user_number = None

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'horizontal_image_path', 'vertical_image', 'ios_main_image']


class HomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        serializer_data = super().to_representation(instance)
        sub_user_id = self.context['sub_user_id']

        queryset = LikeDisLikeMarked.objects.filter(movie=instance.id, sub_user=sub_user_id)

        if queryset:
            marked = queryset.get().marked
        else:
            marked = False
        serializer_data['marked'] = marked

        home_page_list = {'메인 영화': serializer_data}

        """
        재생중인 목록, 
        찜 목록, 
        [ 
            최신등록 상위 10개
            좋아요 상위 10개
            절찬 스트리밍 프리뷰영상 미리보기
        ]
       
        """

        return home_page_list


# 영화 탭에서 영화 장르선택하기 전 화면
class GenreSelectBeforeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'
        depth = 1

    def to_representation(self, instance):
        serializer_data = super().to_representation(instance)
        sub_user_id = self.context['sub_user_id']

        queryset = LikeDisLikeMarked.objects.filter(movie=instance.id, sub_user=sub_user_id)

        if queryset:
            marked = queryset.get().marked
        else:
            marked = False
        serializer_data['marked'] = marked

        # 지정해둔 영화 장르를 넘겨받은 context에서 가져옴
        genre_list = self.context['genre_list']
        genre_movie_list = dict()

        # 장르별 영화 목록을 가져와 dict 으로 만듬
        for genre in genre_list:
            if genre == '외국 영화':
                movie_list = Movie.objects.exclude(like__sub_user=sub_user_id, like__like_or_dislike=2) \
                                 .exclude(genre__name__icontains='한국 영화').distinct()[:18]
            else:
                movie_list = Movie.objects.exclude(like__sub_user=sub_user_id, like__like_or_dislike=2) \
                                 .filter(genre__name__icontains=genre).distinct()[:18]
            movie_list_serializer = MovieSerializer(movie_list, many=True)
            genre_movie_list[genre] = movie_list_serializer.data
        return {'메인 영화': serializer_data, '장르리스트': genre_list, '장르별 영화리스트': genre_movie_list}


# IOS전용 미리보기 시리얼라이저
class PreviewCellListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'circle_image', 'logo_image_path', 'video_file', 'vertical_sample_video_file', ]


# 영화 리스트 시리얼라이저
class MovieListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'id',
            'name',
            'sample_video_file',
            'degree',
            'feature',
            'running_time',
            'horizontal_image_path',
            'vertical_image',
            'original_vertical_image_path',
        ]
        depth = 1


# 영화 상세정보 시리얼라이저
class MovieDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ['view_count', 'like_count', 'created']
        depth = 2

    # def to_representation(self, instance):
        # serializer_data = super().to_representation(instance)
        #
        # sub_user_id = self.context['sub_user_id']
        #
        # like_dislike_marked = LikeDisLikeMarked.objects.filter(movie=instance, sub_user=sub_user_id)
        # if like_dislike_marked:
        #     # 해당 서브유저의 좋아요 정보에 접근해서 찜목록과 좋아요 여부를 확인
        #     # like_dislike_marked = instance.like.filter(sub_user=sub_user_id)[0]
        #     marked = like_dislike_marked[0].marked
        #     like = like_dislike_marked[0].like_or_dislike
        # else:
        #     marked = False
        #     like = 0
        #
        # # 임시적으로 일치율 설정
        # sub_user = SubUser.objects.get(pk=sub_user_id)
        # match_rate = match_rate_calculater(sub_user, instance)
        #
        # # 영화정보의 러닝타임( x시간 x분 형식)과 유저가 이전에 재생을 멈춘시간을 xx분 형식으로 변환해서 남은시간과 총시간을 반환
        #
        # runningtime = instance.running_time
        # if '시간 ' in runningtime:
        #     runningtime = runningtime.split('시간 ')
        #     total_minute = int(runningtime[0]) * 60 + int(runningtime[1][:-1])
        # else:
        #     total_minute = int(runningtime[:-1])
        #
        # if instance.movie_continue.filter(sub_user_id=sub_user_id):
        #     to_be_continue = instance.movie_continue.filter(sub_user_id=sub_user_id)[0].to_be_continue
        #     cur_minute = to_be_continue // 60
        #     remaining_time = total_minute - cur_minute
        # else:
        #     to_be_continue = 0
        #     remaining_time = total_minute
        #
        # # 저장가능 영화인지 확인
        # can_i_store = int(instance.production_date) < 2015
        #
        # # 계산한 값들을 반환할 딕셔너리에 추가
        # key_list = ['marked', 'like', 'match_rate', 'total_minute', 'to_be_continue', 'remaining_time', 'can_i_store']
        # value_list = [marked, like, match_rate, total_minute, to_be_continue, remaining_time, can_i_store]
        #
        # for i in range(len(key_list)):
        #     serializer_data[f'{key_list[i]}'] = value_list[i]
        #
        # # 선택된 영화와 같은 장르를 가진 영화 6개를 골라서 딕셔너리에 추가
        # genre = instance.genre.all()[0]
        # similar_movies = genre.movie.exclude(pk=instance.id)[:6]
        #
        # global sub_user_number
        # sub_user_number = sub_user
        #
        # similar_movies_serializer = SimilarMovieSerializer(similar_movies, many=True)
        #
        # # 골라진 6개의 영화가 서브유저에게 찜되었는지 여부를 확인해서 영화정보 뒤에 추가
        # sub_user_like_all = LikeDisLikeMarked.objects.select_related('movie').filter(sub_user=sub_user_id)
        #
        # for i in range(similar_movies.count()):
        #     for like in sub_user_like_all:
        #         if like.movie == similar_movies[i]:
        #             similar_movies_serializer.data[i]['marked'] = like.marked
        #         else:
        #             similar_movies_serializer.data[i]['marked'] = False
        #
        # serializer_data['similar_movies'] = similar_movies_serializer.data
        # return serializer_data


# 프로필 계정별 찜 목록 시리얼라이저
class MarkedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'horizontal_image_path', 'vertical_image']


# 장르 리스트 시리얼라이저
class GenreListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class MovieOfMovieContinueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'id', 'name', 'video_file', 'logo_image_path', 'horizontal_image_path', 'vertical_image', 'running_time')


class MovieContinueMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'id',
            'name',
            'video_file',
            'logo_image_path',
            'horizontal_image_path',
            'vertical_image',
            'real_running_time',
        )


class MovieContinueSerializer(serializers.ModelSerializer):
    movie = MovieContinueMovieSerializer()

    class Meta:
        model = MovieContinue
        fields = ('movie', 'to_be_continue')

    def to_representation(self, instance):
        serializer_data = super().to_representation(instance)
        sub_user_id = self.context['sub_user_id']

        running_second = instance.movie.real_running_time
        paused_time = instance.to_be_continue

        progress_bar = 100 * paused_time // running_second

        if progress_bar > 100:
            progress_bar = 100

        serializer_data['progress_bar'] = progress_bar
        return serializer_data


class MovieListByGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = (
            'id',
            'name',
            'sample_video_file',
            'logo_image_path',
            'horizontal_image_path',
            'vertical_image',
        )


class BigSizeVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id',
                  'name',
                  'video_file',
                  'horizontal_image_path',
                  'logo_image_path',
                  'synopsis',
                  'big_image_path',
                  'degree',
                  ]
        depth = 1

    def to_representation(self, instance):
        serializer_data = super().to_representation(instance)
        sub_user_id = self.context['sub_user_id']
        try:
            marked_status = instance.like.filter(sub_user_id=sub_user_id)[0].marked
        except IndexError:
            marked_status = False

        serializer_data['marked'] = marked_status

        return serializer_data


class SimilarMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'id',
            'name',
            'degree',
            'synopsis',
            'horizontal_image_path',
            'vertical_image',
            'production_date',
            'running_time',
        ]
        depth = 1

    # def to_representation(self, instance):
    #     serializer_data = super().to_representation(instance)
    #     match_rate = match_rate_calculater(sub_user_number, instance)
    #     serializer_data['match_rate'] = match_rate
    #
    #     return serializer_data
