from rest_framework import viewsets
from api.serializers import StorageSerializer
from api.models import Storage

class StorageViewSet(viewsets.ModelViewSet):
    """Listing all registered Storages"""
    queryset = Storage.objects.all().order_by('-id')
    serializer_class = StorageSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'not implemented'})