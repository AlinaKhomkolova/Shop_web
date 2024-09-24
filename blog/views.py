from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'body', 'image', 'is_published',)
    success_url = reverse_lazy('blog:list')

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание поста'
        return context


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'body', 'image', 'is_published',)

    def get_success_url(self):
        return reverse('blog:view', args=[self.kwargs.get('pk')])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение поста'
        return context

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()

        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        # Фильтруем статьи, которые опубликованы
        return Blog.objects.filter(is_published=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Список постов'
        return context


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.objects = super().get_object(queryset)
        self.objects.views_count += 1
        self.objects.save()

        return self.objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подробности поста'
        return context


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление поста'
        return context
