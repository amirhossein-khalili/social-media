from rest_framework import serializers

from .models import Socialprofile


class SocialprofileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Socialprofile
        fields = "__all__"
