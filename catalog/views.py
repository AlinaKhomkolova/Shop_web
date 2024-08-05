from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, 'catalog/home.html')


def contacts(request):
    return render(request, 'catalog/contacts.html')
