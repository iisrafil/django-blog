from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.urls import reverse


class Site(models.Model):
    name = models.CharField(max_length=30)
    logo = models.ImageField(upload_to="Logo")
    icon = models.ImageField(upload_to="Logo")
    view = models.IntegerField(default=0)


class Category(models.Model):
    name = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='Category_covers')

    def __str__(self):
        return self.name


class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='blog_covers')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    view = models.IntegerField(default=0)
    keywords = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.CharField(max_length=500)


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)

