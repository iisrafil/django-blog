from django.contrib import admin
from .models import Post, Comment, Like, Category, Site

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Site)
