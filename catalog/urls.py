from django.urls import path

from blog.views import BlogCreateView
from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, MenuListView, ProductCreateView, \
    ProductUpdateView, ProductDeleteView, ContactsCreateView, ModeratorProductUpdateView

app_name = CatalogConfig.name

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('blog_form.html', BlogCreateView.as_view(), name='blog_form'),
    path('contacts.html', ContactsCreateView.as_view(), name='contacts'),  # Таблица с контактами
    path('menu.html', MenuListView.as_view(), name='menu'),  # Лист товаров
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),  # Просмотр карточки продукта
    path('create/', ProductCreateView.as_view(), name='create_product'),  # Создание продукта
    path('update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),  # Изменение продукта

    # Изменение продукта для модератора
    path('moderator-update/<int:pk>/', ModeratorProductUpdateView.as_view(), name='moderator_update_product'),

    path('delete_product/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),  # Удаление продукта
]
