from rest_framework import viewsets
from api.serializers import StorageSerializer
from api.models import Storage, Bike, StorageTransfer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

class StorageViewSet(viewsets.ModelViewSet):
    """Listing all registered Storages"""
    queryset = Storage.objects.all().order_by('-id')
    serializer_class = StorageSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({'not implemented'})

    @action(methods=['POST'], detail=False)
    def transfer(self, request):
        """Transfer bikes between storages"""

        destinationId = request.data['destination']
        originId = request.data['origin']

        destinationStorage = get_object_or_404(Storage, pk=destinationId)
        originStorage = get_object_or_404(Storage, pk=originId)

        transferInstance = StorageTransfer.objects.create(
            origin=originStorage,
            destination=destinationStorage
        )

        errors = []

        for bikeId in request.data['bikes']:
            try:
                bike = Bike.objects.get(pk=bikeId)
                bike.storage_place = destinationStorage
                bike.save()
                transferInstance.bikes.add(bike)
            except Bike.DoesNotExist:
                errors.append(bikeId)
        
        transferInstance.save()

        return Response({'message':'Products transferred successfully', 'errors': errors})