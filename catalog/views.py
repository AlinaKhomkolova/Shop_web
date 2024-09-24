from django.forms import inlineformset_factory
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
        active_versions = {}
        products = self.get_queryset()
        for product in products:
            active_version = Version.objects.filter(
                product_id=product.pk, is_active=True
            )
            if active_version:
                product.is_active = active_version.last().name
            else:
                product.is_active = "Активная версия отсутствует"
        context["object_list"] = products

        for product in products:
            active_version = product.versions.filter(is_active=True).first()
            active_versions[product.id] = active_version

        context['active_versions'] = active_versions
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


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:menu')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1
        )
        context['title'] = 'Создание карточки продукта'
        context['version_formset'] = VersionFormset(instance=self.object)
        if self.request.method == "POST":
            context["formset"] = VersionFormset(self.request.POST)
        else:
            context["formset"] = VersionFormset()
        return context

    def form_valid(self, form):
        formset = self.get_context_data()["formset"]
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:menu')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(
            Product, Version, form=VersionForm, extra=1
        )
        context['categories'] = Category.objects.all()  # Добавляем категории в контекст
        context['title'] = 'Изменение карточки продукта'

        if self.request.method == "POST":
            context["formset"] = VersionFormset(
                self.request.POST, instance=self.object
            )
        else:
            context["formset"] = VersionFormset(instance=self.object)
        return context

    def form_valid(self, form):
        formset = self.get_context_data()["formset"]
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:menu')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление продукта'
        return context
