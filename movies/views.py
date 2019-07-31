from django.http import JsonResponse
from django.views import View

from movies.models import Movie


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

