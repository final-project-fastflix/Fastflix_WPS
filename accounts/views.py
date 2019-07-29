from django.http import JsonResponse, HttpResponse
from django.views import View

from accounts.models import ProfileImage, ProfileImageCategory
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


def add_f_category(request):
    images = ProfileImage.objects.all()

    for image in images:
        category_name = image.category
        category_obj = ProfileImageCategory.objects.get_or_create(name=category_name)[0]
        image.f_category = category_obj
        image.save()
