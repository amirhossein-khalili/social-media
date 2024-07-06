from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls", namespace="home")),
    path("api/accounts/", include("accounts.urls", namespace="accounts")),
    #
    #########################################################################
    #
    #######################  social media part and app of it  ###############
    #
    #########################################################################
    #
    path("api/post/", include("post.urls", namespace="post")),
    path("api/socialprofile/", include("socialprofile.urls", namespace="socialprofile")),
    #
    #########################################################################
    #
    ############  this part is for documentation and swagger part ###########
    #
    #########################################################################
    #
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    #
    #########################################################################
    #
    #########################################################################
    #
    #########################################################################
    #
]
