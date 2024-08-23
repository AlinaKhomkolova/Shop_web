from django.urls import path

from catalog.apps import CatalogConfig
from catalog.views import contacts, home

app_name = CatalogConfig.name
urlpatterns = [
    path('', home, name='home'),
    path('contacts.html', contacts, name='contacts'),
]
