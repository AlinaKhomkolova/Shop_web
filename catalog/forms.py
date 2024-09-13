from django import forms

from .models import ContactInfo, Product


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ('email', 'name')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image',
                  'category', 'price',)

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        censorship = ['казино', 'криптовалюта', 'крипта', 'биржа',
                      'дешево', 'бесплатно', 'обман', 'полиция',
                      'радар', ]
        for word in censorship:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Ошибка: Нельзя использовать слово "{word}"')
        return cleaned_data
