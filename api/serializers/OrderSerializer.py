from rest_framework import serializers
from api.models import Order, AdditionalFee
from .AdditionalFeeSerializer import AdditionalFeeSerializer
from .BikeSerializer import BikeSerializer
from .OrderGiftSerializer import OrderGiftSerializer

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.ReadOnlyField(source='customer.name')
    bikes = BikeSerializer(many=True, read_only=True)
    additional_fees = AdditionalFeeSerializer(many=True, read_only=True)
    gifts = OrderGiftSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'