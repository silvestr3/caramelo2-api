from rest_framework import viewsets
from api.serializers import OrderSerializer
from api.models import Order, Customer, Bike, AdditionalFee
from django.utils.timezone import datetime

from rest_framework.response import Response

class OrderViewSet(viewsets.ModelViewSet):
    """Listing all registered Sales"""
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            order_to_delete = Order.objects.get(pk=kwargs['pk'])
        except:
            return Response(status=404)

        for bike in order_to_delete.bikes.all():
            bike.sold = False
            bike.save()

        for fee in order_to_delete.additional_fees.all():
            fee.delete()
        
        try:
            order_to_delete.delete()
            return Response({'status': 'success', 'message': 'order deleted successfully'}, status=200)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=404)

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