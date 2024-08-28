from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, menu, create_product, ProductListView, ProductDetailView

app_name = CatalogConfig.name
urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts.html', contacts, name='contacts'),
    path('menu.html', menu, name='menu'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_description'),
    path('create_product.html', create_product, name='create_product'),
]
