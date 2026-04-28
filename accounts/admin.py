from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin 
from .forms import UserForm

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = UserForm
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'is_admin')
    list_filter = ()
    fieldsets = ()
    filter_horizontal = ()
    ordering = ('-date_joined',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')},
        ),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)