from django.contrib import auth
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# from .models import User


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


# class ResetPasswordRequestSerializer(serializers.Serializer):
#     email = serializers.EmailField(required=True)


# class ResetPasswordSerializer(serializers.Serializer):
#     new_password = serializers.RegexField(
#         regex=r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
#         write_only=True,
#         error_messages={
#             "invalid": (
#                 "رمز عبور باید حداقل 8 کاراکتر با حداقل یک حرف بزرگ و نماد باشد"
#             )
#         },
#     )
#     confirm_password = serializers.CharField(write_only=True, required=True)


# class RegisterSerializer(serializers.ModelSerializer):
#     repeat_password = serializers.CharField(required=True, write_only=True)

#     class Meta:
#         model = User
#         fields = ("username", "password", "email", "repeat_password")
#         extra_kwargs = {"password": {"write_only": True}}

#     def create(self, validated_data):
#         validated_data.pop("repeat_password")
#         user = User.objects.create_user(**validated_data)
#         return user

#     def validate_username(self, value):
#         if value.lower() == "admin":
#             raise serializers.ValidationError("Username can't be 'admin'!!")
#         if User.objects.filter(username=value).exists():
#             raise serializers.ValidationError("This username is already taken!!")
#         return value

#     def validate_email(self, value):
#         if "admin" in value:
#             raise serializers.ValidationError("Email can't contain 'admin'!!")
#         return value

#     def validate(self, data):
#         if data["password"] != data["repeat_password"]:
#             raise serializers.ValidationError(
#                 "Password and repeat password must match!!"
#             )
#         return data


# class LoginSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(max_length=68, min_length=6, write_only=True)
#     username = serializers.CharField(max_length=255, min_length=3)
#     tokens = serializers.SerializerMethodField()

#     def get_tokens(self, obj):
#         user = User.objects.get(username=obj["username"])
#         return {"refresh": user.tokens()["refresh"], "access": user.tokens()["access"]}

#     class Meta:
#         model = User
#         fields = ["password", "username", "tokens"]

#     def validate(self, attrs):
#         username = attrs.get("username", "")
#         password = attrs.get("password", "")
#         user = auth.authenticate(username=username, password=password)
#         if not user:
#             raise AuthenticationFailed("Invalid credentials, try again")
#         if not user.is_active:
#             raise AuthenticationFailed("Account disabled, contact admin")
#         return {"email": user.email, "username": user.username, "tokens": user.tokens}


# class LogoutSerializer(serializers.Serializer):
#     refresh = serializers.CharField()

#     def validate(self, attrs):
#         self.token = attrs["refresh"]
#         return attrs

#     def save(self, **kwargs):
#         try:
#             RefreshToken(self.token).blacklist()
#         except TokenError:
#             self.fail("bad_token")
