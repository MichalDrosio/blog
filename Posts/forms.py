from django import forms
from Posts.models import Post

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['name', 'text', 'author']