from django import forms
from Posts.models import Post, Comment


class AddPostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['name', 'text', 'author', 'image']


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['text', 'author', 'image']


