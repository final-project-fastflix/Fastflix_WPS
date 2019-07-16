from django.urls import path

from .api_view import *

app_name = 'accounts'

urlpatterns = [
    path('create_user', UserCreate.as_view(), name='create_user'),

]