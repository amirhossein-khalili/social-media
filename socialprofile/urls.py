from django.urls import path

from . import views

app_name = "profiles"
urlpatterns = [
    path("list/", views.SocialprofileListView.as_view(), name="list"),
]
