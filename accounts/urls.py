from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

app_name = "accounts"
urlpatterns = [
    path("register/", views.UserRegister.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("signup/step1/", views.SignupStepOneView.as_view(), name="signup_step_one"),
    path("signup/step2/", views.SignupStepTwoView.as_view(), name="signup_step_two"),
    # path("resetPassword/", views.ResetPassword.as_view(), name="reset_password"),
    # path(
    #     "requestPasswordReset/",
    #     views.RequestPasswordReset.as_view(),
    #     name="request_password_reset",
    # ),
]
