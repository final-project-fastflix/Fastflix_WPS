from django.utils import timezone

from accounts.models import SubUser, LikeDisLikeMarked
from movies.models import Movie


def update_real(request):
    movies = Movie.objects.all()
    for movie in movies:
        runningtime = movie.running_time
        if '시간 ' in runningtime:
            runningtime = runningtime.split('시간 ')
            total_minute = int(runningtime[0]) * 60 + int(runningtime[1][:-1])
        else:
            total_minute = int(runningtime[:-1])
        movie.real_running_time = total_minute * 60
        movie.save()


def obj_create(sub_user_id, movie_id):
    sub_user = SubUser.objects.get(id=sub_user_id)
    movie = Movie.objects.get(id=movie_id)

    obj, created = LikeDisLikeMarked.objects.update_or_create(
        movie__name=movie.name,
        sub_user__name=sub_user.name,
        defaults={'movie': Movie.objects.get(name=movie.name),
                  'sub_user': SubUser.objects.get(id=sub_user.id),
                  'updated': timezone.now(),
                  'movie_id': movie_id,
                  'sub_user_id': sub_user_id})
