from django import forms

from .models import ContactInfo, Product, Version


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ('email', 'name')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'description', 'image',
                  'category', 'price',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_name(self):
        cleaned_data = self.cleaned_data['name']
        censorship = ['казино', 'криптовалюта', 'крипта', 'биржа',
                      'дешево', 'бесплатно', 'обман', 'полиция',
                      'радар', ]
        for word in censorship:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Ошибка: Нельзя использовать слово "{word}"')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        censorship = ['казино', 'криптовалюта', 'крипта', 'биржа',
                      'дешево', 'бесплатно', 'обман', 'полиция',
                      'радар', ]
        for word in censorship:
            if word in cleaned_data.lower():
                raise forms.ValidationError(f'Ошибка: Нельзя использовать слово "{word}"')
        return cleaned_data


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
