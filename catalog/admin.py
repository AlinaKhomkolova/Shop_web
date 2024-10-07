from django.contrib import admin

from catalog.models import Product, Category, ContactInfo, Version


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'status', 'user', 'description')
    list_filter = ('category',)
    search_fields = ('name', 'description',)


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
