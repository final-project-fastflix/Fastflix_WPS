from accounts.models import ProfileImage, ProfileImageCategory
from movies.models import *


def add_f_category(request):
    images = ProfileImage.objects.all()

    for image in images:
        category_name = image.category
        category_obj = ProfileImageCategory.objects.get_or_create(name=category_name)[0]
        image.f_category = category_obj
        image.save()
