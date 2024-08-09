from rest_framework import viewsets
from api.serializers import GiftSerializer
from api.models import Gift
from rest_framework.permissions import IsAuthenticated

class GiftViewSet(viewsets.ModelViewSet):
    """Listing all gifts in stock"""
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer
    permission_classes = [IsAuthenticated]