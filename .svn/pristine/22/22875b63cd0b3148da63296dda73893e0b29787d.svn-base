# models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Document(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # descriptionフィールドを追加
    file = models.FileField(upload_to="documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"コメント by {self.author.username} on {self.post.title}"
