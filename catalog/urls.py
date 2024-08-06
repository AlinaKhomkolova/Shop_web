from django.urls import path

from catalog.views import index, contacts, home

urlpatterns = [
    path('', index, name='home'),
    path('home.html', home, name='home'),
    path('contacts.html', contacts, name='contacts'),
]
