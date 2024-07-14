from django.urls import path

from . import views

app_name = "post"
urlpatterns = [
    path("create/", views.PostCreateView.as_view(), name="create"),
    path("list/", views.PostListView.as_view(), name="list"),
    path("search/", views.PostSearchView.as_view(), name="edit"),
    # path("explore/", views.ExploreView.as_view(), name="explore"),
    path("detail/<int:pk>", views.PostDetailView.as_view(), name="detail"),
    path("edit/<int:pk>", views.PostUpdateView.as_view(), name="edit"),
    path("delete/<int:pk>", views.PostDestroyView.as_view(), name="delete"),
    path(
        "comment/<int:post_id>",
        views.CommentCreateView.as_view(),
        name="create-comment",
    ),
    path(
        "comment/<int:comment_id>/reply/",
        views.CommentReplyCreateView.as_view(),
        name="reply-comment",
    ),
    path("like/<int:post_id>", views.LikeCreateView.as_view(), name="like"),
]
