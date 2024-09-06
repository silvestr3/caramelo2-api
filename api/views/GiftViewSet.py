from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from api.serializers import GiftSerializer
from api.models import Gift
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

class GiftViewSet(viewsets.ModelViewSet):
    """Listing all gifts in stock"""
    queryset = Gift.objects.all()
    serializer_class = GiftSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def add(self, request, pk=None):
        """Add products to existing stock"""
        gift = get_object_or_404(Gift, pk=pk)
        try:
            amount = int(request.data.get('amount'))
        except (TypeError, ValueError):
            return Response({"error": "Invalid amount"}, status=400)
        
        # Add the amount to the stock
        gift.stock += amount
        gift.save()

        return Response({"message": f"Added {amount} to stock. New stock: {gift.stock}"}, status=200)