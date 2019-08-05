from django.urls import path
from .api_view import FaceRecommend

urlpatterns = [
    path('', FaceRecommend.as_view(), name='face_reco'),
]