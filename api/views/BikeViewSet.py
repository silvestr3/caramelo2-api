from rest_framework import viewsets
from api.serializers import BikeSerializer
from api.models import Bike, Storage
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date

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
    

    @action(methods=['POST'], detail=False)
    def import_inventory(self, request):
        bikesImport = request.data['bikes']
        storageId = request.data['storage']

        storage = get_object_or_404(Storage, pk=storageId)
        errors = []
        for bike in bikesImport:
            try:
                newInstance = Bike.objects.create(
                model_name=bike['model_name'],
                model_code=bike['model_code'],
                engine=bike['engine'],
                chassi=bike['chassi'],
                registration_plate=bike['registration_plate'],
                color=bike['color'],
                notes=bike['notes'],
                category=bike['category'],
                sale_price=bike['sale_price'],
                brand=bike['brand'],
                storage_place=storage,
                received_date=date.today()
            )

                newInstance.save()
            except Exception as e:
                errors.append(str(e))

        return Response({'message': 'products imported successfully!', 'errors': errors})
