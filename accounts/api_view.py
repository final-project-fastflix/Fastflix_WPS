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
    """
        계정을 만드는 API 입니다
        ---

            - username : 계정이름
            - password : 비밀번호

        return 값은 방금 만든 계정이름과 비밀번호가 리턴됩니다

        요청시 아래와 같이 요청해주시면 됩니다.
        ```
                username : "계정이름"
                password : 패스워드
        ```
    """
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)


# 회원가입이 되면 회원가입 완료 시그널을 받아 토큰을 생성하고 저장한다
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# 기본 계정에 대한 서브유저(프로필계정)을 만드는 뷰
class SubUserCreate(generics.CreateAPIView):
    """
            서브계정(프로필계정)을 만드는 API입니다

        ---

            - name : 계정이름
            - kid : 어린이인지? (true/false)

        return 값은 방금 만든 계정이름과 어린이 여부가 리턴됩니다

        요청시 아래와 같이 요청해주시면 됩니다.
        ```
                user : "계정이름"
                kid : true/false

        ```
    """
    serializer_class = SubUserCreateSerializer

    def perform_create(self, serializer):
        # serializer에 parent_user 속성 추가?
        serializer.save(
            parent_user=self.request.user
        )


# 로그인 API뷰
class Login(APIView):
    """
        로그인 API 입니다

        ---
        ```
        요청시 아래와같이 해주시면 됩니다

        username : 계정
        password : 비밀번호

        로그인 완료시 해당 계정의 토큰이 반환됩니다
        ```
    """
    # 로그인은 인증을 받지 않아도 접속가능
    permission_classes = (AllowAny,)

    def post(self, request):
        if request.method == "POST":
            print(request.META)
            # 넘겨준 데이터를 읽음
            data = request.data
            username = data.get('id')
            password = data.get('pw')

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

