from rest_framework import viewsets
from api.serializers import StorageSerializer
from api.models import Storage

class StorageViewSet(viewsets.ModelViewSet):
    """Listing all registered Storages"""
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer

