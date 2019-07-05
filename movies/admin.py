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