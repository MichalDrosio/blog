from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Post(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    vote = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="home", null=True, blank=True, verbose_name="Zdjęcie")

    def get_absolute_url(self):
        return reverse('posts:post_detail', args=[self.id])

    class Meta:
        ordering = ('-text',)


class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to="home",null=True, blank=True, verbose_name="Zdjęcie")

    class Meta:
        ordering = ('-text',)



class Pictrue(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='files', null=True, blank=True, verbose_name='Zdjęcie')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)