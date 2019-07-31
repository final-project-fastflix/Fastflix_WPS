from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User, SubUser, ProfileImage


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
    profile_info = serializers.SerializerMethodField()

    class Meta:
        model = SubUser
        # fields = '__all__'
        exclude = ['profile_image_path']

    def get_profile_info(self, obj):
        profile_image = ProfileImage.objects.get(image_path=obj.profile_image_path)
        context = {'image_id': profile_image.id, 'profile_image_path': obj.profile_image_path}

        return context


# 서브유저를 만드는 시리얼라이저
class SubUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUser
        fields = ['name', 'kid', ]

    def create(self, validated_data):
        sub_user = SubUser.objects.create(**validated_data)
        sub_user.save()

        return sub_user


# 프로필 계정을 수정하는 시리얼라이저
class SubUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUser
        exclude = ['parent_user']

    def validate_name(self, value):
        if SubUser.objects.filter(
            parent_user=self.instance.parent_user,
            name=value,
        ).exists():

            raise serializers.ValidationError('이미존재하는 이름입니다')
        return value

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            print(attr, value)
            if value:
                setattr(instance, attr, value)
        instance.save()

        return instance


# 프로필 계정을 삭제하는 시리얼라이저
class SubUserDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUser


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


class ChangeProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileImage
        fields = ['name', 'image_path']
