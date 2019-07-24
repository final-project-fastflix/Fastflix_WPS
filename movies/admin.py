from django.contrib import admin

from .models import *

# Register your models here.

admin.site.register(Director)
admin.site.register(Actor)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Feature)
admin.site.register(Degree)


class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'degree',  ]
    search_fields = ['name', 'genre__name', 'degree__name', ]


admin.site.register(Movie, MovieAdmin)


class MovieContinueAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie', 'sub_user', 'to_be_continue']
    list_display_links = ['id', 'movie']


admin.site.register(MovieContinue, MovieContinueAdmin)
