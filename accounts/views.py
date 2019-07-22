from django.http import JsonResponse
from django.views import View

from movies.models import *


class LikeOrDislike(View):
    def post(self, request, *args, **kwargs):
        sub_user = kwargs['sub_user_id']
        movie = Movie.objects.get(pk=kwargs['movie_id'])
        if sub_user in movie.likes.all():
            movie.likes.remove(sub_user)
            return JsonResponse({'data': 'remove'})
        else:
            movie.likes.add(sub_user)
            return JsonResponse({'data': 'add'})

