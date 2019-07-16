from django.db.models import signals
from rest_framework import serializers

from .models import User


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
