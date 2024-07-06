from django.urls import path

from . import views

app_name = "post"
urlpatterns = [
    path("create/", views.PostCreateView.as_view(), name="create"),
    path("edit/<int:pk>", views.PostUpdateView.as_view(), name="edit"),
    path("list/", views.PostListView.as_view(), name="list"),
    path("explore/", views.ExploreView.as_view(), name="explore"),
]
