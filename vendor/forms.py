from django.contrib.auth.forms import UserCreationForm
from .models import Vendor
from accounts.models import User
from django import forms

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name', 'license']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tasty Bites', 'id': 'restaurant_name'}),
            'license': forms.FileInput(attrs={'class': 'form-control', 'id': 'license'})
        }