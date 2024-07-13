from django.contrib import admin

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("slug", "user", "created", "updated")
    search_fields = ("user__username", "content")
    list_filter = ("created", "updated")
    prepopulated_fields = {"slug": ("user", "content")}
    raw_id_fields = ("user",)


@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    list_display = ("user", "post", "created", "is_reply")
    raw_id_fields = ("user", "post", "reply")
