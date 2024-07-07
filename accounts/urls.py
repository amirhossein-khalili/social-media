from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView

from . import views

app_name = "accounts"
urlpatterns = [
    path("register/", views.UserRegister.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("resetPassword/", views.ResetPassword.as_view(), name="reset_password"),
    # path(
    #     "requestPasswordReset/",
    #     views.RequestPasswordReset.as_view(),
    #     name="request_password_reset",
    # ),
]
