from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    ##################### profile part #####################
    bio = models.CharField(max_length=200)
    followers_count = models.IntegerField(default=0)
    followings_count = models.IntegerField(default=0)
    posts_count = models.IntegerField(default=0)
    description = models.CharField(max_length=200)
    is_private = models.BooleanField(default=False)
    activate = models.BooleanField(default=True)
    is_reported = models.BooleanField(default=False)
    #########################################################
