from django.contrib import admin

from catalog.models import Product, Category, ContactInfo, Version


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'status', 'user', 'description')
    list_filter = ('category',)
    search_fields = ('name', 'description',)

    permissions = [
        ('can_change_product_status', 'Может изменять статус продукта'),
        ('can_change_product_description', 'Может изменять описание продукта'),
        ('can_change_product_category', 'Может изменять категорию продукта'),
    ]

    def get_readonly_fields(self, request, obj=None):
        """
        Устанавливаю поля только для чтения в зависимости от прав пользователя.
        """
        readonly_fields = super().get_readonly_fields(request, obj)

        # Разрешить изменение статуса только если у пользователя есть соответствующее право
        if not request.user.has_perm('catalog.can_change_product_status'):
            readonly_fields = readonly_fields + ('status',)

        # Разрешить изменение описания только если у пользователя есть соответствующее право
        if not request.user.has_perm('catalog.can_change_product_description'):
            readonly_fields = readonly_fields + ('description',)

        # Разрешить изменение категории только если у пользователя есть соответствующее право
        if not request.user.has_perm('catalog.can_change_product_category'):
            readonly_fields = readonly_fields + ('category',)

        return readonly_fields

    def has_change_permission(self, request, obj=None):
        """
        Проверка, есть ли у пользователя право на изменение продукта в целом.
        """
        if super().has_change_permission(request, obj):
            return True

            # Проверка кастомных прав на изменение отдельных полей
        return (
                request.user.has_perm('catalog.can_change_product_status') or
                request.user.has_perm('catalog.can_change_product_description') or
                request.user.has_perm('catalog.can_change_product_category')
        )

    def save_model(self, request, obj, form, change):
        """
        Сохраняем только те поля, на которые у пользователя есть права.
        """
        # Загружаем объект из базы данных для сравнения
        original_obj = Product.objects.get(pk=obj.pk)

        # Проверяем и обновляем описание, если у пользователя есть разрешение
        if request.user.has_perm('catalog.can_change_product_description'):
            obj.description = form.cleaned_data.get('description', obj.description)
        else:
            obj.description = original_obj.description  # Оставляем оригинальное описание

        # Проверяем и обновляем категорию, если у пользователя есть разрешение
        if request.user.has_perm('catalog.can_change_product_category'):
            obj.category = form.cleaned_data.get('category', obj.category)
        else:
            obj.category = original_obj.category  # Оставляем оригинальную категорию

        # Проверяем и обновляем статус, если у пользователя есть разрешение
        if request.user.has_perm('catalog.can_change_product_status'):
            obj.status = form.cleaned_data.get('status', obj.status)
        else:
            obj.status = original_obj.status  # Оставляем оригинальный статус

        # Оставляем другие поля неизменными, если нет разрешений
        obj.name = original_obj.name
        obj.price = original_obj.price

        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'created_at')
    search_fields = ('name', 'email')


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'version_number', 'version_name', 'is_active')
    list_filter = ('version_number',)
    search_fields = ('version_name', 'version_number',)
