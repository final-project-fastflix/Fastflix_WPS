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

# @permission_classes((AllowAny,))
# def get_token(request):
#     print(request.data)
#     username = request.POST.get('username')
#     user_id = User.objects.get(username=username).id
#     token = Token.objects.get(user_id=user_id).key
#
#     context = {'token': token}
#
#     return JsonResponse(context)
#
#     # return render(request, 'accounts/forms.html', context={'form': form})
#
