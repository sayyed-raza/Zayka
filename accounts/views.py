from django.shortcuts import render, redirect, reverse
from django.views import View
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

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
            utils.send_verification_email(request, user)
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
        utils.send_verification_email(request, user)
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

def activate(request, uidb64, token):
    """Activate the user account if the token is valid."""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated successfully!")
        return redirect('dashboard')
    else:
        messages.error(request, "Activation link is invalid!")
        return redirect('login')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            utils.send_password_reset_email(request, user)
            messages.success(request, "Password reset link has been sent to your email.")
            return redirect('login')
        except User.DoesNotExist:
            messages.error(request, "No user found with this email address.")
    return render(request, 'accounts/forgot-password.html')

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['reset_user_id'] = uid  # Store user ID in session for the next step
        return redirect('reset-password')
    else:
        messages.error(request, "Password reset link is invalid!")
        return redirect('forgot-password')

def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('reset-password')

        user_id = request.session.get('reset_user_id')
        if user_id:
            try:
                user = User.objects.get(pk=user_id)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password has been reset successfully!")
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, "User does not exist!")
        else:
            messages.error(request, "Session expired! Please try again.")
    return render(request, 'accounts/reset-password.html')