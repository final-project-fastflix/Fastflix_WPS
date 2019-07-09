from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Director)
admin.site.register(Actor)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Feature)
admin.site.register(Degree)
admin.site.register(Movie)

class MovieContinueAdmin(admin.ModelAdmin):
    models = MovieContinue
    # list_display = ['movie_id', 'sub_user_id', 'to_be_continue']

admin.site.register(MovieContinue, MovieContinueAdmin)