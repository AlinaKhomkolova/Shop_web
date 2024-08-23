from django.shortcuts import render, redirect, get_object_or_404

from catalog.forms import ContactForm
from catalog.models import Product, Category, ContactInfo


# Create your views here.
def home(request):
    # Получаем список всех категорий
    categories = Category.objects.all()

    # Фильтрация продуктов по категории, если она выбрана
    category_id = request.GET.get('category')
    if category_id:
        cocktails = Product.objects.filter(category_id=category_id)
    else:
        cocktails = Product.objects.all()

    return render(request, 'catalog/home.html', {
        'cocktails': cocktails,
        'categories': categories,
        'title': 'Главная',
    })


def menu(request):
    # Получаем список всех категорий
    categories = Category.objects.all()

    # Фильтрация продуктов по категории, если она выбрана
    category_id = request.GET.get('category')
    if category_id:
        cocktails = Product.objects.filter(category_id=category_id)
    else:
        cocktails = Product.objects.all()

    return render(request, 'catalog/menu.html', {
        'cocktails': cocktails,
        'title': 'Меню',
    })


def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Сохраняем данные в базу данных
            return redirect(request.path)  # Перенаправляем на ту же страницу
    else:
        form = ContactForm()

    contacts_data = ContactInfo.objects.all()  # Получаем все контакты из базы данных
    return render(request, 'catalog/contacts.html', {
        'form': form,
        'contacts': contacts_data,
        'title': 'Контактная информация',
    })


def product_description(request, id):
    product = get_object_or_404(Product, id=id)

    return render(request, 'catalog/product_description.html', {
        'title': 'Описание напитка',
        'product': product
    })
