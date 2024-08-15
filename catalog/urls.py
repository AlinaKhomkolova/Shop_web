from django.urls import path
from catalog.views import contacts, home

urlpatterns = [
    path('', home, name='home'),
    path('contacts.html', contacts, name='contacts'),
]
