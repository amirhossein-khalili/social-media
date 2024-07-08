from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ("username", "password", "email", "repeat_password")
        extra_kwargs = {
            "password": {"write_only": True},
        }

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
        if "admin" in value:
            raise serializers.ValidationError("Email can't contain 'admin' !!")
        return value

    def validate(self, data):
        if data["password"] != data["repeat_password"]:
            raise serializers.ValidationError(
                "Password and repeat password must match!!"
            )
        return data


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
        if "admin" in value:
            raise serializers.ValidationError("Email can't contain 'admin' !!")
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
