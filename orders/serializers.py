from rest_framework import serializers
from .models import RepairOrder


class RepairOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairOrder
        fields = "__all__"
        read_only_fields = ("status", "total_amount")