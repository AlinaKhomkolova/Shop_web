from django import forms

from blog.models import Blog


class BlogForm(forms.ModelForm):

    class Meta:
        model = Blog
        fields = (
            'title', 'body',
            'image', 'views_count', 'is_published',)
