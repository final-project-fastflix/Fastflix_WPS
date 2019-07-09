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
        contact=openapi.Contact(email="Jay@google.com"),
        license=openapi.License(name="WPS의 FastFlix 문서"),
    ),
    validators=['flex'], #'ssv'],
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_v1_patterns,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')),
    # 스웨거 API 문서
    path('swagger/.json/', schema_view_v1.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/v1/', schema_view_v1.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/v1/', schema_view_v1.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
