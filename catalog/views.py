from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from catalog.forms import ContactForm, ProductForm
from catalog.models import Product, Category, ContactInfo


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Главная'
        return data


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_description.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Описание'
        return data


class MenuListView(ListView):
    model = Product
    template_name = 'catalog/menu.html'
    context_object_name = 'page_obj'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['categories'] = Category.objects.all()
        data['title'] = 'Меню'
        return data


class ContactsView(View):
    template_name = 'catalog/contacts.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        contacts_data = ContactInfo.objects.all()  # Получаем все контакты из базы данных
        return render(request, self.template_name, {
            'form': form,
            'contacts': contacts_data,
            'title': 'Контактная информация',
        })

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем данные в базу данных
            return redirect(request.path)  # Перенаправляем на ту же страницу

        contacts_data = ContactInfo.objects.all()  # Получаем все контакты из базы данных
        return render(request, self.template_name, {
            'form': form,
            'contacts': contacts_data,
            'title': 'Контактная информация',
        })


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:menu')  # Перенаправляем на ту же страницу

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Добавляем категории в контекст
        context['title'] = 'Создание карточки продукта'
        return context


class ProductUpdateView(UpdateView):
    pass
