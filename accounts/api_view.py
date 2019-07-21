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
            - email : 이메일
            - password : 비밀번호

        return 값은 방금 만든 계정이름과 비밀번호가 리턴됩니다

        요청시 아래와 같이 요청해주시면 됩니다.
        ```
        Body에 email과 password를 넣어서 보내주시면 됩니다
            email : 이메일
            password : 비밀번호
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


class SubUserCreate(APIView):
    """
                서브계정(프로필계정)을 만드는 API입니다

            ---

                - name : 프로필이름
                - kid : 어린이인지? (true/false)

            성공할 경우 return 값은 처음 입력한 프로필의 ID 값 을 리턴합니다.
            ※ 프로필 이름이 이미 등록되어 있는경우 'error' : 0을 리턴합니다

            요청시 아래와 같이 요청해주시면 됩니다.
            ```
                헤더에 Authorization : Token '토큰값' 을 넣어주세요
                Body에 user와 kid를 넣어서 보내주시면 됩니다

                만약 여러개의 데이터를 넣고싶으신 경우 아래와 같이 보내주시면 됩니다.

                요청시 :
                {
                    "name": ["이름1", "이름2", "이름3", "이름4"]
                    "kid": ["false", "true", "false", "false"]
                }


                리턴값:
                {
                    "id": 이름1의 ID값
                }

                    name : 프로필이름
                    kid : true/false

            ```
        """

    def post(self, request, *args, **kwargs):
        # 프로필계정을 5개를 초과할 수 없음
        # 기존 등록 되어있는 프로필계정의 목록
        sub_user_list = SubUser.objects.filter(parent_user_id=request.user.id)

        if len(sub_user_list) >= 5:
            return JsonResponse(data={'error': '프로필을 더이상 만들 수 없습니다.'},
                                status=status.HTTP_406_NOT_ACCEPTABLE)

        # 바디 형
        username = request.data.get('name')

        kids = request.data.get('kid')

        # 이름을 비교하기 위한 리스트
        # 기존 프로필 계정 목록에서 이름만 가져온 리스트
        sub_user_name_list = []
        for sub_user in sub_user_list:
            sub_user_name_list.append(sub_user.name)

        # 입력한 username이 여러개인 경우
        if isinstance(username, list):

            for index in range(len(username)):

                if username[index] in sub_user_name_list:
                    return JsonResponse(data={'error': False}, status=status.HTTP_403_FORBIDDEN)

                serializer = SubUserCreateSerializer(
                    data={'name': username[index], 'kid': kids[index]}
                )
                if serializer.is_valid():
                    serializer.save(parent_user=request.user)

            return JsonResponse(data={'id': SubUser.objects.get(name=username[0]).id}, status=status.HTTP_200_OK)

        # 1개 인 경우
        else:
            if username in sub_user_name_list:
                return JsonResponse(data={'error': False}, status=status.HTTP_403_FORBIDDEN)

            serializer = SubUserCreateSerializer(
                data={'name': username, 'kid': kids}
            )
            if serializer.is_valid():
                serializer.save(parent_user=request.user)

            return JsonResponse(data={'id': SubUser.objects.get(name=username).id}, status=status.HTTP_200_OK)


class SubUserList(generics.ListAPIView):
    """
                계정에 속한 모든 프로필을 보여주는 API입니다

            ---

                - name : 프로필이름
                - kid : 어린이인지? (true/false)

            return 값은 계정에 속한 모든 프로필을 리턴합니다

            ```
                해당 URL로 헤더에 Authorization : Token '토큰값' 을 넣어주세요

            ```
        """

    serializer_class = SubUserListSerializer

    def get_queryset(self):
        queryset = SubUser.objects.filter(parent_user_id=self.request.user.id)

        return queryset


# 로그인 API뷰
class Login(APIView):
    """
        로그인 API 입니다

        ---
        ```
        바디에 넣어서 보내주시면 됩니다

        id : 가입시 Email
        pw : 비밀번호

        로그인 완료시 해당 계정의 토큰이 반환됩니다
        ```
    """
    # 로그인은 인증을 받지 않아도 접속가능
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        # 헤더 형
        # username = request.META.get('HTTP_ID')
        # password = request.META.get('HTTP_PW')

        # 바디 형1 -> request.POST로도 가능하나 request.data가 좀더 유연한 방식이다
        # username = request.POST.get('id')
        # password = request.POST.get('pw')

        # 바디 형2
        username = request.data.get('id')
        password = request.data.get('pw')

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
