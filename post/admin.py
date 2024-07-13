from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("slug", "author", "created", "updated")
    search_fields = ("author__username", "content")
    list_filter = ("created", "updated")
    prepopulated_fields = {"slug": ("author", "content")}
    raw_id_fields = ("author",)
