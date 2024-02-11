from rest_framework import viewsets
from rest_framework.decorators import action
from api.serializers import OrderSerializer
from api.models import Order, Customer, Bike, AdditionalFee
from django.utils.timezone import datetime
from django.shortcuts import get_object_or_404

from rest_framework.response import Response

class OrderViewSet(viewsets.ModelViewSet):
    """Listing all registered Sales"""
    serializer_class = OrderSerializer

    def get_queryset(self):
        queryset = Order.objects.all().order_by('-id')
        customer = self.request.query_params.get('customer')

        if customer is not None:
            filtercustomer = get_object_or_404(Customer, pk=customer)
            queryset = queryset.filter(customer=filtercustomer)

        return queryset
    

    def update(self, request, *args, **kwargs):
        order_to_edit = Order.objects.get(pk=kwargs['pk'])
        
        #editing single fields
        order_to_edit.notes = request.data['notes']
        order_to_edit.payment_method = request.data['paymentMethod']
        order_to_edit.discount = request.data['discount']
        order_to_edit.down_payment = request.data['downPayment']
        order_to_edit.total = request.data['total']
        order_to_edit.total_price = request.data['total']

        #editing bike price
        bike_to_edit = order_to_edit.bikes.all()[0]
        bike_to_edit.sale_price = request.data['bikePrice']
        bike_to_edit.save()

        #editing additional fees
        for old_fee in order_to_edit.additional_fees.all():
            order_to_edit.additional_fees.remove(old_fee)
            old_fee.delete()

        for new_fee in request.data['additionalFees']:
            create_fee = AdditionalFee.objects.create(
                description=new_fee['description'],
                amount=new_fee['amount']
            )
            order_to_edit.additional_fees.add(create_fee)
            create_fee.save()

        order_to_edit.save()
        return Response({'message': 'order edited!'}, status=200)


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
    
    @action(methods=['GET'], detail=False)
    def latest(self, request):
        queryset = self.get_queryset()[:6]
        serializer = OrderSerializer(queryset, many=True)

        return Response(serializer.data)