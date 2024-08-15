from django import forms
from .models import ContactInfo


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['email', 'name']
