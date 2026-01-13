from django.urls import path
from .webhooks import PaymentWebhookAPIView

urlpatterns = [
    path("webhooks/payment/", PaymentWebhookAPIView.as_view()),
]