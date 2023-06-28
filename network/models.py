from django.contrib.auth.models import AbstractUser
from django.db import models

from django.utils import timezone


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, default=None, related_name="post"
    )
    created_at = models.DateTimeField(default=timezone.now)
    text = models.TextField(default="")
    likes = models.ManyToManyField(User, related_name="likes")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    followers = models.ManyToManyField(User, related_name="followers")
    following = models.ManyToManyField(User, related_name="following")
