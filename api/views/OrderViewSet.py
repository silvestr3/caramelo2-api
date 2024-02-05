from rest_framework import viewsets
from api.serializers import OrderSerializer
from api.models import Order, Customer, Bike, AdditionalFee
from django.utils.timezone import datetime

from rest_framework.response import Response

class OrderViewSet(viewsets.ModelViewSet):
    """Listing all registered Sales"""
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer

    def create(self, request):
        customer = Customer.objects.filter(pk=request.data["customer"])[0]

        new_order = Order.objects.create(
            sale_date= datetime.today(),
            customer= customer,

            total_price= request.data['total'],
            discount= request.data['discount'],
            down_payment= request.data['down_payment'],
            total=request.data['total'],

            payment_method=request.data['payment_method'],
            notes= request.data['notes'],
            registration_status= 'CPL',
            has_checkout= True
        )

        for bike in request.data['bikes']:
            instance = Bike.objects.filter(pk=bike['id'])[0]
            instance.sold = True
            instance.save()
            new_order.bikes.add(instance)

        for fee in request.data['additional_fees']:
            instance = AdditionalFee.objects.create(
                description=fee["description"],
                amount=fee['amount']
            )

            new_order.additional_fees.add(instance)
            instance.save()
        
        new_order.save()

        return Response({"success": True, "message": "order placed successfully"})