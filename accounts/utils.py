from .models import User

def check_user_role(user):
    if user.role == User.CUSTOMER:
        return 'customer-dashboard'
    elif user.role == User.RESTAURANT_OWNER:
        return 'vendor-dashboard'
    elif user.is_staff or user.is_admin or user.is_superadmin or user.role is None:
        return 'admin:index'
    