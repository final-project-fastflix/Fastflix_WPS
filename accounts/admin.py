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


class LikeDisLikeMaredAdmin(admin.ModelAdmin):
    list_display_links = ['movie', ]
    list_editable = ['like_or_dislike', 'marked', ]
    list_display = ['sub_user', 'movie', 'like_or_dislike',
                    'marked', 'created', 'updated', ]


admin.site.register(LikeDisLikeMarked, LikeDisLikeMaredAdmin)

admin.site.register(ProfileImage)