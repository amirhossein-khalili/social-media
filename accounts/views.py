from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserRegisterSerializer


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


# class RequestPasswordReset(generics.GenericAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = ResetPasswordRequestSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         email = request.data["email"]
#         user = User.objects.filter(email__iexact=email).first()

#         if user:
#             token_generator = PasswordResetTokenGenerator()
#             token = token_generator.make_token(user)
#             reset = PasswordReset(email=email, token=token)
#             reset.save()

#             reset_url = f"{os.environ['PASSWORD_RESET_BASE_URL']}/{token}"

#             # Sending reset link via email (commented out for clarity)
#             # ... (email sending code)

#             return Response(
#                 {"success": "We have sent you a link to reset your password"},
#                 status=status.HTTP_200_OK,
#             )
#         else:
#             return Response(
#                 {"error": "User with credentials not found"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )


# class RegisterView(generics.GenericAPIView):
#     serializer_class = RegisterSerializer

#     def post(self, request):
#         user = request.data
#         serializer = self.serializer_class(data=user)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         user_data = serializer.data
#         return Response(user_data, status=status.HTTP_201_CREATED)


# class LoginAPIView(generics.GenericAPIView):
#     serializer_class = LoginSerializer

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class LogoutAPIView(generics.GenericAPIView):
#     serializer_class = LogoutSerializer
#     permission_classes = (permissions.IsAuthenticated,)

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(status=status.HTTP_204_NO_CONTENT)
