from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect

from .forms import UserForm
from.models import User



# Create your views here.
# def register(request):
#     return render(request, 'accounts/register-user.html', {
#         "form": UserForm,
#     })

class RegisterView(View):
    def get(self, request):
        return render(request, 'accounts/register-user.html', {
            "form": UserForm(),
        })

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            user.save()
            messages.success(request, "User registered successfully!")
            return redirect('register')
        return render(request, 'accounts/register-user.html', {
            "form": form,
        })