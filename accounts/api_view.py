from django.contrib.auth import authenticate, login
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import *


# 회원가입 API
class UserCreate(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


# 회원가입이 되면 회원가입 완료 시그널을 받아 토큰을 생성하고 저장한다
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# 기본 계정에 대한 서브유저(프로필계정)을 만드는 뷰
class SubUserCreate(generics.CreateAPIView):
    serializer_class = SubUserCreateSerializer

    def perform_create(self, serializer):
        # serializer에 parent_user 속성 추가?
        serializer.save(
            parent_user=self.request.user
        )


# 로그인 API뷰
class UserLogin(APIView):
    # 로그인은 인증을 받지 않아도 접속가능
    permission_classes = (AllowAny,)

    def post(self, request):
        if request.method == "POST":
            # 넘겨준 데이터를 읽음
            data = request.data
            username = data.get('username', None)
            password = data.get('password', None)

            # 해당하는 유저가 있는지 확인
            user = authenticate(username=username, password=password)

            if user is not None:
                # 유저가 로그인 가능한 권한이 있으면 로그인함
                if user.is_active:
                    login(request, user)

                    # 받은 정보로 토큰을 돌려준다
                    user_id = User.objects.get(username=username).id
                    token = Token.objects.get(user_id=user_id).key

                    context = {'token': token}

                    return JsonResponse(context, status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(status=status.HTTP_404_NOT_FOUND)
