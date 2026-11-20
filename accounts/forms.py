from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password1', 'password2',]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'John', 'id': 'firstname'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Doe', 'id': 'lastname'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'johndoe', 'id': 'username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'john@example.com', 'required': True, 'id': 'email'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0000000000', 'id': 'phone'}),
        }

# !Creates a new email field instead of adding class and placeholder to the existing username field. This is because AuthenticationForm uses 'username' as the field name for authentication, and we want to keep that intact while customizing its widget to look like an email input. If we added a new 'email' field, it would not be used for authentication and would cause confusion. 
# class LoginForm(AuthenticationForm):
#     email = forms.EmailField(widget=forms.EmailInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Email Address',
#         'id': 'email',
#     }))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={
#         'class': 'form-control',
#         'placeholder': 'Password',
#         'id': 'password',
#     }))
#     class Meta:
#         model = User
#         fields = ['email', 'password']


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        # Call the parent class's __init__ method first to generate the default fields
        super(LoginForm, self).__init__(*args, **kwargs)
        
        # Now, customize the existing 'username' field (which acts as your email)
        self.fields['username'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email Address',
            'id': 'email',
        })
        
        # Customize the existing 'password' field
        self.fields['password'].widget = forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'password',
        })