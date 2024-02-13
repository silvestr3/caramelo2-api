from rest_framework import viewsets
from api.serializers import BikeSerializer
from api.models import Bike, Storage
from django.shortcuts import get_object_or_404

class BikeViewSet(viewsets.ModelViewSet):
    """Listing all registered bikes in stock"""
    serializer_class = BikeSerializer
    
    def get_queryset(self):
        queryset = Bike.objects.all().order_by('-id')

        storage_id = self.request.query_params.get('storage')

        if storage_id is not None:
            filterStorage = get_object_or_404(Storage, pk=storage_id)
            queryset = queryset.filter(storage_place=filterStorage).filter(sold=False)

        return queryset
    

