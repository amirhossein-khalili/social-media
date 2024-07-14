from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

app_name = "accounts"
urlpatterns = [
    # ==================================================
    #  Authentication
    # ==================================================
    path("login/", views.LoginView.as_view(), name="token_obtain_pair"),
    path("signup/step1/", views.SignupStepOneView.as_view(), name="signup_step_one"),
    path("signup/step2/", views.SignupStepTwoView.as_view(), name="signup_step_two"),
    # ==================================================
    #   Profile Part
    # ==================================================
    path(
        "profile/<str:action>/<int:user_id>/",
        views.FollowUnfollowView.as_view(),
        name="follow-unfollow",
    ),
    path(
        "profile/",
        views.ProfileUpdateView.as_view(),
        name="edit_profile",
    ),
    path(
        "profile/<int:pk>/",
        views.ProfileUserView.as_view(),
        name="user_profile",
    ),
    # ==================================================
]
