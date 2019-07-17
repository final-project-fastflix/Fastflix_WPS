from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User, SubUser


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data.get('password'))
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class SubUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUser
        fields = ['name', 'kid', ]

    def create(self, validated_data):
        sub_user = SubUser.objects.create(**validated_data)
        sub_user.save()

        return sub_user


class GetTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ['user_id', 'key']


class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', ]