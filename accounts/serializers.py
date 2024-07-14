from typing import Any, Dict

from django.contrib import auth
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from post.serializers import PostSerializer

from .models import User

# ==================================================
#   Authentication
# ==================================================


class SignupStepOneSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128)
    repeat_password = serializers.CharField(max_length=128)

    def create(self, validated_data):
        validated_data.pop("repeat_password")
        user = User.objects.create_user(**validated_data)
        return user

    def validate_username(self, value):
        if value.lower() == "admin":
            raise serializers.ValidationError("Username can't be 'admin'!!")
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username is already taken!!")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already taken!!")
        return value

    def validate(self, data):
        if data["password"] != data["repeat_password"]:
            raise serializers.ValidationError(
                "Password and repeat password must match!!"
            )
        return data


class SignupStepTwoSerializer(serializers.Serializer):

    email = serializers.EmailField()

    code = serializers.CharField(max_length=6)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "your signup is completed please use the login option"
            )
        return value


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs: Dict[str, Any]) -> Dict[str, str]:
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=username, password=password
        )

        if not user:
            raise serializers.ValidationError(
                "No active account found with the given credentials"
            )

        refresh = self.get_token(user)

        data = {}
        data["login-token"] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, user)

        return data


# ==================================================
#   Profile Part
# ==================================================


class ProfileSerializer(serializers.ModelSerializer):

    followers_count = serializers.SerializerMethodField(read_only=True)
    followings_count = serializers.SerializerMethodField(read_only=True)
    posts_count = serializers.SerializerMethodField(read_only=True)
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "bio",
            "email",
            "followers_count",
            "followings_count",
            "posts_count",
            "posts",
        ]

    def get_followers_count(self, obj):
        return obj.get_followers_count()

    def get_followings_count(self, obj):
        return obj.get_followings_count()

    def get_posts_count(self, obj):
        return obj.get_posts_count()


# ==================================================
