from django.shortcuts import render
from rest_framework import viewsets
from .models import Webhook
from .serializers import WebhookSerializer
from django_filters.rest_framework import DjangoFilterBackend

class WebhookViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Webhook CRUD. (Covers Story 4)
    """
    queryset = Webhook.objects.all()
    serializer_class = WebhookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event_type', 'is_active']
