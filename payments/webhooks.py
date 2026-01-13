import hmac
import hashlib
import os

from rest_framework.views import APIView
from rest_framework.response import Response

from orders.models import RepairOrder
from .models import PaymentEvent


class PaymentWebhookAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        payload = request.body
        signature = request.headers.get("X-Signature")
        secret = os.getenv("WEBHOOK_SECRET")

        expected_signature = hmac.new(
            secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        if signature != expected_signature:
            return Response({"error": "Invalid signature"}, status=400)

        event_id = request.data["event_id"]
        order_id = request.data["order_id"]
        amount = request.data["amount"]

        if PaymentEvent.objects.filter(event_id=event_id).exists():
            return Response(status=200)

        order = RepairOrder.objects.get(order_id=order_id)

        if float(amount) != float(order.total_amount):
            return Response({"error": "Amount mismatch"}, status=400)

        order.status = "paid"
        order.save()

        PaymentEvent.objects.create(event_id=event_id)

        return Response({"status": "payment confirmed"})