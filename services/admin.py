from django.contrib import admin
from .models import Service, ServiceVariant


class ServiceVariantInline(admin.TabularInline):
    model = ServiceVariant
    extra = 1


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "vendor")
    inlines = [ServiceVariantInline]