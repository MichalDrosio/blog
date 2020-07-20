from django.db import models

# Create your models here.

class Post(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=30)