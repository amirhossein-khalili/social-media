import logging

import redis
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import code_generator, redis_instance

from .serializers import (
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
    serializer_class = SignupStepOneSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            data = data = request.data
            email = data["email"]

            verification_code = self.send_verification_code(email)

            return Response(
                {"message": "Verification code sent to email"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_verification_code(self, user_email):
        try:
            code = code_generator()

            print(
                "verification in the amir social media",
                f"this is your verification code babe :  {code}",
                "amirhossein.khalili.supn@gmail.com",
                [user_email],
            )
            send_mail(
                "verification in the amir social media",
                f"this is your verification code babe :  {code}",
                "amirhossein.khalili.supn@gmail.com",
                [user_email],
                fail_silently=False,
            )

            print(
                "_" * 50,
                "\n",
                code,
                "\n",
                "_" * 50,
            )

            return code

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return Response(
                {"error": "Failed to send verification code. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SignupStepTwoView(APIView):
    def post(self, request):
        serializer = SignupStepTwoSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            code = serializer.validated_data["code"]

            # Retrieve data from Redis
            user_data = redis_instance.get(email)
            if not user_data:
                return Response(
                    {"error": "Verification code expired or invalid"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            username, password, stored_code = user_data.decode("utf-8").split("|")
            if code != stored_code:
                return Response(
                    {"error": "Invalid verification code"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create the user
            User.objects.create_user(username=username, email=email, password=password)

            # Delete the data from Redis
            redis_instance.delete(email)

            return Response(
                {"message": "User created successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
