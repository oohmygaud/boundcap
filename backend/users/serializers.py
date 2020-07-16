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
    allowed_users = serializers.SerializerMethodField()
    
    def get_allowed_users(self, obj):
       return UserAllowedEntitySerializer(obj.permissions.all(), many=True).data
    
    class Meta:
        model = Entity
        fields = [
            "id",
            "title",
            "allowed_users"
        ]


class UserAllowedEntitySerializer(serializers.ModelSerializer):
    user_data = serializers.SerializerMethodField()

    def get_user_data(self, obj):
        return UserSerializer(obj.user).data
    

    class Meta:
        model = UserAllowedEntity
        fields = [
            "id",
            "user",
            "user_data",
            "entity"
        ]
        