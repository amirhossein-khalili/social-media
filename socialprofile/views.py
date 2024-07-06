from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Socialprofile
from .serializers import SocialprofileSerializer


class SocialprofileListView(generics.ListAPIView):
    serializer_class = SocialprofileSerializer
    queryset = Socialprofile.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]
