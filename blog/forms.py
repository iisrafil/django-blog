from django import forms
from blog.models import Post


class postCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'content', 'cover_image','keywords')

