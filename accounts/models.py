from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.


# class User(AbstractUser):
#     email = models.EmailField(max_length=255, unique=True, db_index=True)
#     phone_number = models.CharField(max_length=20, unique=True, db_index=True)
#     dial_number = models.CharField(max_length=20)
#     groups = models.ManyToManyField(Group, related_name="custom_user_set")
#     user_permissions = models.ManyToManyField(
#         Permission, related_name="custom_user_set"
#     )

#     def __str__(self):
#         return self.username

#     def tokens(self):
#         refresh = RefreshToken.for_user(self)
#         return {"refresh": str(refresh), "access": str(refresh.access_token)}
