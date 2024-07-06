from rest_framework import serializers

from .models import Post

# class PostSerializer(serializers.ModelSerializer):
#     author = serializers.SerializerMethodField()

#     class Meta:
#         model = Post
#         fields = ["id", "content", "image", "created_at", "updated_at", "author"]
#         read_only_fields = ["created_at", "updated_at", "author"]


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "content",
            "slug",
            "image",
            "created_at",
            "updated_at",
        ]

    def validate_content(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "Content must be at least 10 characters long."
            )
        return value

    def get_author(self, obj):
        return {"username": obj.author.username, "email": obj.author.email}
