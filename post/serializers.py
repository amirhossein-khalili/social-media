from rest_framework import serializers

from .models import Comment, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["id", "user", "content", "slug", "image", "created", "updated"]

    def validate_content(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                "Content must be at least 10 characters long."
            )
        return value

    def get_url(self, obj):
        request = self.context.get("request")
        return request.build_absolute_uri(obj.get_absolute_url())


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "user", "body", "created", "is_reply", "reply"]
        read_only_fields = ["id", "user", "created"]

    def validate(self, data):
        if data.get("is_reply") and not data.get("reply"):
            raise serializers.ValidationError(
                "Reply field is required if is_reply is True"
            )
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = {
            "username": instance.user.username,
            "email": instance.user.email,
        }

        if instance.reply is not None:
            representation["reply"] = {
                "body": instance.reply.body,
                "created": instance.reply.created,
                "is_reply": instance.reply.is_reply,
                "reply": instance.reply.reply,
            }
        else:
            representation["reply"] = None

        return representation


class PostDetailSerializer(serializers.ModelSerializer):
    postcomments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "content",
            "slug",
            "image",
            "created",
            "updated",
            "postcomments",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user"] = {
            "username": instance.user.username,
            "email": instance.user.email,
        }

        representation["user"] = {
            "username": instance.user.username,
            "email": instance.user.email,
        }
        return representation
