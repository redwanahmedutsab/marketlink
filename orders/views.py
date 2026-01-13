from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from services.models import ServiceVariant
from .models import RepairOrder


class CreateOrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        variant_id = request.data.get("variant_id")

        with transaction.atomic():
            variant = ServiceVariant.objects.select_for_update().get(id=variant_id)

            if variant.stock < 1:
                return Response({"error": "Out of stock"}, status=400)

            variant.stock -= 1
            variant.save()

            order = RepairOrder.objects.create(
                customer=request.user,
                vendor=variant.service.vendor,
                variant=variant,
                total_amount=variant.price,
            )

        return Response({
            "order_id": order.order_id,
            "payment_url": f"https://fake-payment.com/pay/{order.order_id}"
        })