from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, MenuListView, ContactsView, CreateProduct

app_name = CatalogConfig.name
urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts.html', ContactsView.as_view(), name='contacts'),
    path('menu.html', MenuListView.as_view(), name='menu'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_description'),
    path('create_product.html', CreateProduct.as_view(), name='create_product'),
]
