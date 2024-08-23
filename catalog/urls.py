from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, home, menu, product_description

app_name = CatalogConfig.name
urlpatterns = [
    path('', home, name='home'),
    path('contacts.html', contacts, name='contacts'),
    path('menu.html', menu, name='menu'),
    path('product/<int:id>/', product_description, name='product_description'),
]
