from rest_framework import viewsets
from api.serializers import CustomerSerializer
from api.models import Customer
from rest_framework.permissions import IsAuthenticated

class CustomerViewSet(viewsets.ModelViewSet):
    """Listing all registered customers"""
    queryset = Customer.objects.all().order_by('-id')
    serializer_class = CustomerSerializer
    # permission_classes = [IsAuthenticated]

