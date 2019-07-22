from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User, SubUser


# 계정을 만드는 시리얼라이저
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['email'],
                                   email=validated_data['email'],
                                   password=validated_data['password'], )
        user.set_password(validated_data.get('password'))
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


# 프로필 계정 목록을 보여주는 시리얼라이저
class SubUserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUser
        fields = '__all__'


# 서브유저를 만드는 시리얼라이저
class SubUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUser
        fields = ['name', 'kid', ]

    def create(self, validated_data):
        sub_user = SubUser.objects.create(**validated_data)
        sub_user.save()

        return sub_user


# 토큰을 얻는 시리얼라이저
class GetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['user_id', 'key']


# 로그인을 하는 시리얼라이저
class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', ]
