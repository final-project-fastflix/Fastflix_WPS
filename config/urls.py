"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

# 스웨거 API 문서
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_url_v1_patterns = [
    path('movies/', include('movies.urls', namespace='movies_api')),
]


schema_view_v1 = get_schema_view(
    openapi.Info(
        title="FastFlix API",
        default_version='v1',
        description="WPS의 FastFlix API 문서 페이지 입니다.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="sug5806@gmail.com"),
        license=openapi.License(name="WPS의 FastFlix 문서"),
    ),
    validators=['flex'], #'ssv'],
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_v1_patterns,
)

urlpatterns = [
    path('config_site/', admin.site.urls),
    path('movies/', include('movies.urls')),
  
    # 스웨거 API 문서

    # 이 주소를 입력하자 마자 다운로드가 됨 json 파일인데 쓸일은 없을듯싶음
    path('swagger/.json/', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),

    # swagger/v1/로 접속하면 기존 swagger 기능이 가능한 API 문서?
    path('swagger/v1/', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # docs/v1/로 접속하면 API 목록이 한눈에 들어오는 API 문서가 나옴 깔-끔함
    path('docs/v1/', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
