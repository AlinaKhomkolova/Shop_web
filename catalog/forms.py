from django import forms

from .models import ContactInfo, Product


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['email', 'name']


class CreateProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image',
                  'category', 'price',
                  ]
