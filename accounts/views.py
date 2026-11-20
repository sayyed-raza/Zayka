from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required

from .forms import UserForm, LoginForm
from .models import User
from vendor.forms import VendorForm
from .decorators import vendor_only, customer_only
from . import utils

def home(request):
    return render(request, 'home.html')
# Create your views here.
# def register(request):
#     return render(request, 'accounts/register-user.html', {
#         "form": UserForm,
#     })

class RegisterUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already registered and logged in!")
            return redirect('dashboard')
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
            return redirect('login')
        return render(request, 'accounts/register-user.html', {
            "form": form,
        })
    
def register_vendor(request):
    if request.user.is_authenticated and request.user.role == User.RESTAURANT_OWNER:
        messages.info(request, "You are already registered and logged in!")
        return redirect('dashboard')
    form = UserForm(request.POST or None)
    v_form = VendorForm(request.POST or None, request.FILES or None)
    if form.is_valid() and v_form.is_valid(): 

        # !This should be done in a transaction to ensure atomicity, but for simplicity, we are doing it sequentially here.
        user = form.save(commit=False)
        user.role = User.RESTAURANT_OWNER
        user.save()
        vendor = v_form.save(commit=False)
        vendor.user = user
        vendor.user_profile = user.user_profile
        vendor.save()
        messages.success(request, "Vendor registered successfully! Please wait for approval.")
        return redirect('dashboard')
    return render(request, 'accounts/register-vendor.html', {
        "form": form,
        "v_form": v_form,
    })


def login(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect('dashboard')
    form = LoginForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()  # This will get the user object, but you need to log them in using Django's login function
        if user is not None and user.is_active:
            auth_login(request, user)  # This will log the user in and create a session for them
            messages.success(request, "Logged in successfully!")
            return redirect('dashboard')  
    return render(request, 'accounts/login.html', {
        "form": form,
    })

@login_required(login_url='login')
def logout(request):
    if request.user.is_authenticated and request.method == "POST":
        auth_logout(request)
        messages.info(request, "Logged out successfully!")
    return redirect('login')


# ?This is not a good practice as the functions grow for each dashboard, this view would become too big.
# @login_required(login_url='login')
# def profile(request):
#     if not request.user.is_authenticated:
#         messages.error(request, "You need to be logged in to view your profile!")
#         return redirect('login')
#     else:
#         if request.user.is_restaurant_owner():
#             return render(request, 'accounts/vendor-dashboard.html')
#         else:
#             return render(request, 'accounts/user-dashboard.html')
#         # elif request.user.role == User.DELIVERY_PERSONNEL:
#         #     return render(request, 'accounts/delivery-dashboard.html')

@login_required(login_url='login')
def profile(request):
    user_redirect= utils.check_user_role(request.user)
    return redirect(user_redirect)

@customer_only
def customer_profile(request):
    return render(request, 'accounts/customer-dashboard.html')

@vendor_only
def vendor_profile(request):
    return render(request, 'accounts/vendor-dashboard.html')