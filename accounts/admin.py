from django.contrib import admin

from .models import *


# Register your models here.

class SubUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent_user']
    list_display_links = ['name']


admin.site.register(SubUser, SubUserAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'is_staff', 'is_superuser', 'auth_token']
    list_display_links = ['username']
    list_editable = ['is_staff', 'is_superuser', ]


admin.site.register(User, UserAdmin)


class LikeDisLikeMarkedAdmin(admin.ModelAdmin):
    list_display_links = ['movie', ]
    list_editable = ['like_or_dislike', 'marked', ]
    list_display = ['sub_user', 'movie', 'movie_id', 'like_or_dislike',
                    'marked', 'created', 'updated', ]


admin.site.register(LikeDisLikeMarked, LikeDisLikeMarkedAdmin)


class ProfileImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'image_path', 'f_category']
    list_display_links = ['id', 'name', ]


admin.site.register(ProfileImage, ProfileImageAdmin)

admin.site.register(ProfileImageCategory)