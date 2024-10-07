from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ContactForm, ProductForm, VersionForm
from catalog.models import Product, Category, ContactInfo, Version


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Главная'
        return data


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'

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
        context = super().get_context_data(**kwargs)
        products = context['page_obj']

        active_versions = Version.objects.filter(is_active=True, product__in=products)

        version_dict = {version.product_id: version.version_name for version in active_versions}

        for product in products:
            product.active_version = version_dict.get(product.pk, "Активная версия отсутствует")

        context["object_list"] = products
        context['active_versions'] = version_dict
        context['categories'] = Category.objects.all()
        context['title'] = 'Меню'

        return context


class ContactsCreateView(CreateView):
    model = ContactInfo
    template_name = 'catalog/contacts.html'
    success_url = reverse_lazy('catalog:contacts')
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contacts'] = ContactInfo.objects.all()  # Добавляем категории в контекст
        context['title'] = 'Контактная информация'
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:menu')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Пожалуйста, войдите в систему или зарегистрируйтесь, чтобы создать продукт.')
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1
        )

        if self.request.method == "POST":
            context["formset"] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context["formset"] = VersionFormset(instance=self.object)

        context['title'] = 'Создание карточки продукта'

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        # Привязка текущего пользователя к создаваемому продукту
        form.instance.user = self.request.user
        # Сохранение объекта
        self.object = form.save()
        # проверка валидности formset и сохраняем его
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:menu')
    permission_required = (
        'catalog.change_product_status',
        'catalog.change_product_description',
        'catalog.change_product_category',
    )

    def get_permission_object(self):
        return self.get_object()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Пожалуйста, войдите в систему или зарегистрируйтесь, чтобы изменить продукт.')
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ProductForm = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1
        )

        if self.request.method == "POST":
            context["formset"] = ProductForm(
                self.request.POST, instance=self.object
            )
        else:
            context["formset"] = ProductForm(instance=self.object)

        context['categories'] = Category.objects.all()
        context['title'] = 'Изменение карточки продукта'

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context["formset"]
        # Сохранение объекта
        self.object = form.save()
        # проверка валидности formset и сохраняем его
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:menu')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Пожалуйста, войдите в систему или зарегистрируйтесь, чтобы удалить продукт.')
            return redirect('users:login')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление продукта'
        return context
