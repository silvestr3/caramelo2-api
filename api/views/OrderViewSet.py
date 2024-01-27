from rest_framework import viewsets
from api.serializers import OrderSerializer
from api.models import Order

class OrderViewSet(viewsets.ModelViewSet):
    """Listing all registered Sales"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

