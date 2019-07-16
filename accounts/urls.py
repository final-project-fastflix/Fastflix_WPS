from django.urls import path

from .views import *

app_name = 'accounts'

urlpatterns = [
    path('create_user', UserCreate.as_view(), name='create_user'),

]