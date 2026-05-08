from django.contrib import admin

from .models import Vendor

# Register your models here.
class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('user__email', 'name')
    readonly_fields = ("rating",)

admin.site.register(Vendor, VendorAdmin)