from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)

    bio = models.CharField(max_length=200, blank=True)
    posts_count = models.IntegerField(default=0)
    description = models.CharField(max_length=200, blank=True)
    is_private = models.BooleanField(default=False)
    activate = models.BooleanField(default=True)
    is_reported = models.BooleanField(default=False)

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def get_followers_count(self):
        return User.objects.filter(following_relations__to_user=self).count()

    def get_followers(self):
        return User.objects.filter(following_relations__to_user=self)

    def get_followings_count(self):
        return User.objects.filter(follower_relations__from_user=self).count()

    def get_followings(self):
        return User.objects.filter(follower_relations__from_user=self)


class Relation(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following_relations",
    )

    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower_relations",
    )

    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "relation"
        verbose_name_plural = "relations"
