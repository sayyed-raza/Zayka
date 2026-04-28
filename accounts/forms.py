from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User

class UserForm(UserCreationForm):

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Create a password',
            'id': 'password',
        }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password',
            'id': 'confirm_password',
    }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John', 'id': 'firstname'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe', 'id': 'lastname'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'johndoe', 'id': 'username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john@example.com', 'required': True, 'id': 'email'}),
        }