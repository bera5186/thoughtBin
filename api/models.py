from django.db import models
import uuid

from authMiddleware.models import User

# Create your models here.
class Post(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, serialize=True
    )
    title = models.CharField(max_length=400, db_index=True, null=False)
    text = models.TextField(max_length=6000, null=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    slug = models.CharField(
        max_length=400, unique=True, db_index=True, default=uuid.uuid4
    )
    private = models.BooleanField(default=False)
    claps = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.slug


class Comment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, serialize=True
    )
    comment = models.TextField(max_length=1000, null=False)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author_reply = models.TextField(
        max_length=1000, default=None, null=True, blank=True
    )
    is_liked_by_author = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)


class Clap(models.Model):
    class Meta:
        unique_together = (("user", "post"),)

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, serialize=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    claps = models.BigIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user} {self.post} {self.claps}"
