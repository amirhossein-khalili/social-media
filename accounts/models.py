from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    email = models.EmailField(unique=True)


# class Socialprofile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     bio = models.TextField(blank=True, null=True)
#     profile_image = models.ImageField(
#         upload_to="profile_images/", blank=True, null=True
#     )

#     def __str__(self):
#         return f"{self.user.username}'s Profile"
