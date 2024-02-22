from rest_framework import generics
from api.serializers import StorageTransferSerializer
from api.models import StorageTransfer
from rest_framework.permissions import IsAuthenticated


class StorageTransferList(generics.ListAPIView):
    """Listings Storage transfer history"""
    serializer_class = StorageTransferSerializer
    http_method_names = ['get']
    # permission_classes = [IsAuthenticated]


    def get_queryset(self):
        queryset = StorageTransfer.objects.all().order_by('-id')
        
        startDate = self.request.query_params.get('startDate')
        endDate = self.request.query_params.get('endDate')
        
        if startDate is not None and endDate is not None:
            queryset = queryset.filter(transfer_date__range=[startDate, endDate])
            

        return queryset
    
