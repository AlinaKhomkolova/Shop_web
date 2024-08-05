from django.urls import path

from catalog.views import index, contacts

urlpatterns = [
    path('home.html', index),
    path('contacts.html', contacts),
]
