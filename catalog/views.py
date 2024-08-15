from django.shortcuts import render
from catalog.models import Product, Category


# Create your views here.
def home(request):
    check_info(request)

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
    })

def contacts(request):
    check_info(request)
    return render(request, 'catalog/contacts.html')


def check_info(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        print(f'{name.title()}\n'
              f'E-mail: {email}')
