from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import User

def vendor_only(function):
    """Decorator to restrict access to views for users with the role of RESTAURANT_OWNER only."""
    @wraps(function)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if request.user.role == User.RESTAURANT_OWNER:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied("You are not authorized to access this page.")
            # messages.error(request, "You are not authorized to access that page.")
            # return redirect('dashboard')
    return wrapper

def customer_only(function):
    """Decorator to restrict access to views for users with the role of CUSTOMER only."""
    @wraps(function)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):
        if request.user.role == User.CUSTOMER:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied("You are not authorized to access this page.")
            # messages.error(request, "You are not authorized to access that page.")
            # return redirect('dashboard')
    return wrapper