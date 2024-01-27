from rest_framework import viewsets
from api.serializers import BikeSerializer
from api.models import Bike

class BikeViewSet(viewsets.ModelViewSet):
    """Listing all registered bikes in stock"""
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer

