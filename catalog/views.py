from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.forms import inlineformset_factory
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.forms import ContactForm, ProductForm, VersionForm, ModeratorProductForm
from catalog.models import Product, Category, ContactInfo, Version
from catalog.services import get_cached_categories


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

    def get_object(self, queryset=None):
        if settings.CACHE_ENABLED:
            cache_key = f'product_detail_{self.kwargs["pk"]}'
            product = cache.get(cache_key)

            if product is None:  # Если продукта нет в кэше
                product = super().get_object(queryset)
                cache.set(cache_key, product)  # Сохраняем продукт в кэш

            return product

        return super().get_object(queryset)  # Если кэш не включен, возвращаем объект без кэширования


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
        context['categories'] = get_cached_categories()
        context['title'] = 'Меню'

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
        'catalog.can_change_product_status',
        'catalog.can_change_product_description',
        'catalog.can_change_product_category',)

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if self.request.user != obj.user:
            print(f'User: {self.request.user}, Permissions: {self.request.user.get_all_permissions()}')

            if not self.request.user.has_perms(self.permission_required):
                print('Permission denied: У пользователя нет необходимых разрешений')
                raise PermissionDenied

        return obj

    def has_permission(self):
        # Проверка прав для текущего пользователя
        return (
                self.request.user.has_perm('catalog.can_change_product_status') or
                self.request.user.has_perm('catalog.can_change_product_description') or
                self.request.user.has_perm('catalog.can_change_product_category') or
                self.request.user == self.get_object().user  # Позволить владельцу редактировать
        )

    def get_permission_object(self):
        return self.get_object()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Пожалуйста, войдите в систему или зарегистрируйтесь, чтобы изменить продукт.')
            return redirect('users:login')

        if not self.has_permission():
            messages.error(request, 'У вас нет доступа к этой странице.')
            return redirect('catalog:menu')

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

    def get_form_class(self):
        user = self.request.user
        if self.object.user == user:
            return ProductForm
        if user.has_perm("catalog.can_change_product_status") and user.has_perm(
                "catalog.can_change_product_description") and user.has_perm(
            "catalog.can_change_product_category"):
            return ModeratorProductForm
        raise PermissionDenied

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


class ModeratorProductUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ModeratorProductForm
    template_name = 'catalog/moderator_product_form.html'
    success_url = reverse_lazy('catalog:menu')
    permission_required = (
        'catalog.can_change_product_status',
        'catalog.can_change_product_description',
        'catalog.can_change_product_category',
    )

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj


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
