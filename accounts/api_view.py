from django.contrib.auth import authenticate, login
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from .serializer import *


# 회원가입 API
class UserCreate(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 넘어온 데이터값이 유효하다면
        # serializer의 create 함수를 실행시킨다
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        # 회원가입된 유저의 id값을 가져온다
        created_user_id = serializer.data['id']

        # 가져온 id값을 바탕으로 토큰값을 가져온다
        context = {
            'Token': Token.objects.get(user_id=created_user_id).key
        }

        # serializer.data는 클래스의 속성이므로 변경할수 없다
        # 새로운 dict을 만들고 context를 추가한 다음에 serializer.data를 추가한다
        new_dict = context
        new_dict.update(serializer.data)

        return Response(new_dict, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


# 회원가입이 되면 회원가입 완료 시그널을 받아 토큰을 생성하고 저장한다
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class SubUserCreate(generics.CreateAPIView):
    serializer_class = SubUserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(serializer)
        serializer.is_valid(raise_exception=True)

        # 넘어온 데이터값이 유효하다면
        # serializer의 create 함수를 실행시킨다
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
