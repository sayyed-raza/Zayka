from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect

from .forms import UserForm
from.models import User
from vendor.forms import VendorForm


# Create your views here.
# def register(request):
#     return render(request, 'accounts/register-user.html', {
#         "form": UserForm,
#     })

class RegisterUserView(View):
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
    
def register_vendor(request):
    form = UserForm(request.POST or None)
    v_form = VendorForm(request.POST or None, request.FILES or None)
    if form.is_valid() and v_form.is_valid(): 
        user = form.save(commit=False)
        user.role = User.RESTAURANT_OWNER
        user.save()
        vendor = v_form.save(commit=False)
        vendor.user = user
        vendor.user_profile = user.user_profile
        vendor.save()
        messages.success(request, "Vendor registered successfully! Please wait for approval.")
        return HttpResponseRedirect(reverse('register-vendor'))
    return render(request, 'accounts/register-vendor.html', {
        "form": form,
        "v_form": v_form,
    })