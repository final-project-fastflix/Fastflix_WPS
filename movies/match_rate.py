import math
import operator
from collections import Counter

from accounts.models import LikeDisLikeMarked
from movies.models import Movie


def match_rate_calculater(sub_user, target):
    marked_objs = LikeDisLikeMarked.objects.select_related(
        'movie',
    ).prefetch_related(
        'movie__actors',
        'movie__directors',
        'movie__genre',
    ).filter(marked=True, sub_user=sub_user)

    # target = Movie.objects.get(pk=404)

    target_actors = target.actors.values_list('name', flat=True)
    target_directors = target.directors.values_list('name', flat=True)
    target_genres = target.genre.values_list('name', flat=True)

    marked_movies_name_counter = Counter(marked_objs.values_list('movie__name', flat=True))
    marked_movie_actors_name_counter = Counter(marked_objs.values_list('movie__actors__name', flat=True))
    marked_movie_directors_name_counter = Counter(marked_objs.values_list('movie__directors__name', flat=True))
    marked_movie_genres_name_counter = Counter(marked_objs.values_list('movie__genre__name', flat=True))

    actor_grade = calculate_premium_grade(marked_movie_actors_name_counter, target_actors)
    director_grade = calculate_premium_grade(marked_movie_directors_name_counter, target_directors)
    genre_grade = calculate_premium_grade(marked_movie_genres_name_counter, target_genres)

    weight_table = {'1': 8, '2': 7, '3': 6, '4': 5, '5': 0}

    actor_point = weight_table[
        calculate_normal_grade(actor_grade, target_actors, marked_movie_actors_name_counter)]

    genre_point = weight_table[
        calculate_normal_grade(genre_grade, target_genres, marked_movie_genres_name_counter)]

    director_point = weight_table[calculate_normal_grade(director_grade, target_directors,
                                                              marked_movie_directors_name_counter)]

    match_rate = 50 + actor_point * 2 + genre_point * 3 + director_point

    return match_rate


def calculate_premium_grade(counter, target):
    sorted_by_key = {}

    for item in counter.items():
        if item[1] in sorted_by_key:
            sorted_by_key[item[1]].append(item[0])
        else:
            sorted_by_key[item[1]] = [item[0]]

    sorted_list = sorted(sorted_by_key.items(), key=operator.itemgetter(0))
    premium_list = [sorted_list.pop() for _ in range(math.ceil(len(sorted_list) / 2))]

    total_count = 0

    for i in premium_list:
        w = i[0]
        count = 0
        for j in target:
            if j in i[1]:
                count += 1
        total_count += count * w

    if total_count >= target.count():
        return '1'
    elif total_count > target.count() // 2:
        return '2'
    else:
        return None


def calculate_normal_grade(grade, target, counter):
    if grade:
        return grade
    else:
        total_count = sum([counter.get(name, 0) for name in target])

        if total_count >= target.count():
            return '2'
        elif total_count > target.count() // 5:
            return '3'
        elif total_count:
            return '4'
        else:
            return '5'
