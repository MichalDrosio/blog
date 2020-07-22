from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Post(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)