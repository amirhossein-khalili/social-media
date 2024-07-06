from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from permissions import IsOwnerReadOnly


class Home(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        return Response(data={"message": "hello world"}, status=status.HTTP_200_OK)

    def post(self, request):

        return Response(data={"message": "hello world"}, status=status.HTTP_200_OK)
