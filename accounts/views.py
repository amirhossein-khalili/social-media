import logging

import redis
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from utils import code_generator, redis_instance

from .models import User
from .serializers import (
    CustomTokenObtainPairSerializer,
    SignupStepOneSerializer,
    SignupStepTwoSerializer,
    UserRegisterSerializer,
)

logger = logging.getLogger(__name__)


class UserRegister(APIView):

    serializer_class = UserRegisterSerializer

    def post(self, request):

        ser_data = UserRegisterSerializer(data=request.data)

        if ser_data.is_valid():

            user = ser_data.create(ser_data.validated_data)

            return Response(
                {"message": "User created successfully", "user": ser_data.data},
                status=status.HTTP_201_CREATED,
            )

        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class SignupStepOneView(APIView):
    """
    in this part first we check the user data

    and if the user data is valid then we save the user data

    in the cache and send a verification code to user email

    the user data have 1 hour expiration but the verification

    code have only 3 minutes expiration .

    """

    serializer_class = SignupStepOneSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]

            verification_code = self.send_verification_code(email)

            if verification_code:

                cache.set(
                    f"signup_{email}_user_data",
                    serializer.validated_data,
                    3600,
                )

                cache.set(
                    f"signup_{email}_verification_code",
                    verification_code,
                    180,
                )

                return Response(
                    {"message": "Verification code sent to email"},
                    status=status.HTTP_200_OK,
                )

            else:
                return Response(
                    {
                        "error": "Failed to send verification code. Please try again later."
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_verification_code(self, user_email):
        try:
            code = code_generator()

            send_mail(
                "Verification in the Amir Social Media",
                f"This is your verification code: {code}",
                "amirhossein.khalili.supn@gmail.com",
                [user_email],
                fail_silently=False,
            )

            return code

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return None


class SignupStepTwoView(APIView):
    """

    in this section we get and check if user data exist in the cache

    then we check if the code that user add be true and valid

    if code time passed and the code is expired but the user data is not expired

    then we create a new code and send it to user and set the new code to cache

    after that if the user will be created and data will remove from the cache

    if user not exists in the cache: he should again complete the first step of the verification

    """

    serializer_class = SignupStepTwoSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            code = serializer.validated_data["code"]

            user_data = cache.get(f"signup_{email}_user_data")

            if user_data:

                code_data = cache.get(f"signup_{email}_verification_code")

                if not code_data:
                    verification_code = self.send_verification_code(email)

                    if verification_code:

                        cache.set(
                            f"signup_{email}_verification_code",
                            verification_code,
                            180,
                        )

                        return Response(
                            {
                                "message": "your code has been expired , we send it to you again !!",
                            },
                            status=status.HTTP_200_OK,
                        )

                    else:
                        return Response(
                            {
                                "error": "Failed to send verification code. Please try again later."
                            },
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        )

                if code == code_data:

                    # create user and complete the signup process
                    User.objects.create(
                        username=user_data["username"],
                        email=user_data["email"],
                        password=user_data["password"],
                    )

                    # delete user data from cache
                    cache.delete(f"signup_{email}_user_data")
                    cache.delete(f"signup_{email}_verification_code")

                else:

                    return Response(
                        {"error": "Verification code expired or invalid"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            if not user_data:
                return Response(
                    {"error": "please first sign up the first step !!"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {"message": "you had signup successfully 🥳🎉."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_verification_code(self, user_email):
        try:
            code = code_generator()

            send_mail(
                "Verification in the Amir Social Media",
                f"This is your verification code: {code}",
                "amirhossein.khalili.supn@gmail.com",
                [user_email],
                fail_silently=False,
            )

            return code

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return None


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
