from rest_framework import generics
from api.serializers import CustomerOrdersSerializer
from api.models import Order


class CustomerOrdersList(generics.ListAPIView):
    """Listings all orders from given user"""
    serializer_class = CustomerOrdersSerializer

    def get_queryset(self):
        queryset = Order.objects.filter(customer=self.kwargs['pk'])
        return queryset
