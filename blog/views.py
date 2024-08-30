from django.urls import reverse_lazy
from django.views.generic import UpdateView

from blog.models import Blog


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'body')
    success_url = reverse_lazy('blog:list')