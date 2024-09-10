from django.urls import path

from blog.views import BlogCreateView
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, MenuListView, ContactsView, ProductCreateView, \
    ProductUpdateView

app_name = CatalogConfig.name
urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts.html', ContactsView.as_view(), name='contacts'),
    path('menu.html', MenuListView.as_view(), name='menu'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_description'),
    path('create/', ProductCreateView.as_view(), name='create_product'),
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('blog_form.html', BlogCreateView.as_view(), name='blog_form'),
]
