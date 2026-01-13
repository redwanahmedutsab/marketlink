import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from orders.models import RepairOrder

class PaymentWebhook(APIView):
    authentication_classes = []

    def post(self, request):
        payload = request.data
        event_id = payload.get("event_id")

        if RepairOrder.objects.filter(order_id=payload["order_id"], status='paid').exists():
            return Response({"status": "ignored"})

        order = RepairOrder.objects.get(order_id=payload["order_id"])

        if float(payload["amount"]) != float(order.total_amount):
            return Response({"error": "Amount mismatch"}, status=400)

        order.status = 'paid'
        order.save()

        return Response({"status": "success"})