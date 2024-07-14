from django.conf import settings
from django.db import models


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    content = models.TextField()
    slug = models.SlugField(max_length=20, default=None)
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post by {self.user.username} at {self.created}"

    def likes_count(self):
        return self.plikes.count()

    def get_absolute_url(self):
        return reverse("post:detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["content"]


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="usercomments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="postcomments"
    )
    reply = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="replycomments",
        blank=True,
        null=True,
    )
    is_reply = models.BooleanField(default=False)
    body = models.TextField(max_length=400)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.id}"

    def likes_count(self):
        return self.plikes.count()


class Like(models.Model):

    # class VoteType(models.TextChoices):
    #     LIKE = "like", "Like"
    #     DISLIKE = "dislike", "Dislike"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ulikes"
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="plikes")
    # type = models.CharField(
    #     max_length=7,
    #     choices=VoteType.choices,
    #     default=VoteType.LIKE,
    # )

    def __str__(self):
        return f"{self.user} - {self.post}"
