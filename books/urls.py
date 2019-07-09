from django.urls import path, include


urlpatterns =[
    # other urls
    path('', include('haystack.urls')),
]