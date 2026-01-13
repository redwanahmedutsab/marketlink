from django.contrib import admin
from .models import RepairOrder


@admin.register(RepairOrder)
class RepairOrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "customer", "vendor", "status", "total_amount")
    list_filter = ("status",)
    readonly_fields = ("order_id", "created_at")