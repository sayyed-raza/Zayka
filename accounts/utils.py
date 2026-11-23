from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode

from .models import User
from django.conf import settings

def check_user_role(user):
    if user.role == User.CUSTOMER:
        return 'customer-dashboard'
    elif user.role == User.RESTAURANT_OWNER:
        return 'vendor-dashboard'
    elif user.is_staff or user.is_admin or user.is_superadmin or user.role is None:
        return 'admin:index'


def send_verification_email(request,user):
    """Sends a verification email to the user with an activation link."""
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    message = render_to_string('accounts/emails/activate_account.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(mail_subject, message, from_email=from_email, to=[to_email])
    # email.send(using=settings.MAILERS['smtp']['BACKEND'], fail_silently=False)
    email.send()

def send_password_reset_email(request, user):
    """Sends a password reset email to the user with a reset link."""
    from_email = settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    mail_subject = 'Reset your password.'
    message = render_to_string('accounts/emails/reset-password.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    email = EmailMessage(mail_subject, message, from_email=from_email, to=[to_email])
    email.send()