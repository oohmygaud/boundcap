from rest_framework import serializers
from .models import User, Entity, UserAllowedEntity
from rest_registration.api.serializers import DefaultRegisterUserSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "username", "password")

class RegisterUserSerializer(DefaultRegisterUserSerializer):
    email = serializers.EmailField(required=True)

class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ("__all__")

class UserAllowedEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAllowedEntity
        fields = ("__all__")