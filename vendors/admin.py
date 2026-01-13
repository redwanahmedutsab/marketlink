from django.contrib import admin
from .models import VendorProfile


@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ("business_name", "user", "is_active")
    list_filter = ("is_active",)
    search_fields = ("business_name",)