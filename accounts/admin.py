from django.contrib import admin

from .models import *


# Register your models here.

class SubUserAdmin(admin.ModelAdmin):
    pass


admin.site.register(SubUser, SubUserAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'is_staff', 'is_superuser', 'auth_token']
    list_display_links = ['username']
    list_editable = ['is_staff', 'is_superuser', ]


admin.site.register(User, UserAdmin)

admin.site.register(LikeDisLikeMarked)
