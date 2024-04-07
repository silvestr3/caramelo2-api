from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.db.models.functions import ExtractMonth, ExtractYear
from django.db.models import Count, Sum
from calendar import month_name
from rest_framework.permissions import IsAuthenticated

from api.models import Order, Bike


################################################ SALES ###################################################


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sales_volume(request):
    """Sales per month"""
    sales_per_month = Order.objects.all().annotate(
        year=ExtractYear('sale_date'),
        month=ExtractMonth('sale_date'),
    ).values('year', 'month').annotate(
        total_sales=Count('id'),
        total_revenue=Sum('total'),
    ).order_by('year', 'month')

    monthly_data = list(sales_per_month.values('year', 'month', 'total_sales', 'total_revenue'))

    month_dict = {i: month_name[i] for i in range(1, 13)}
    for data in monthly_data:
        data['month'] = month_dict[data['month']]

    return Response({"data": monthly_data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sales_payment_method(request):
    """Sales per payment method"""
    sales_by_payment_method = Order.objects.values('payment_method').annotate(
        total_sales=Count('id'),
        total_revenue=Sum('total'),
    ).order_by('-total_sales')

    return Response({"data": sales_by_payment_method})



################################################ INVENTORY ################################################

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inventory_volume(request):
    """Bikes received per month"""
    bikes_per_month = Bike.objects.all().annotate(
        year=ExtractYear('received_date'),
        month=ExtractMonth('received_date'),
    ).values('year', 'month').annotate(
        total_bikes=Count('id')
    ).order_by('year', 'month')
    
    bikes_monthly_data = list(bikes_per_month.values('year', 'month', 'total_bikes'))
    month_dict = {i: month_name[i] for i in range(1, 13)}

    for data in bikes_monthly_data:
        if 'month' in data and data['month'] is not None:
            data['month'] = month_dict[data['month']]

        
    return Response({"data": bikes_monthly_data})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inventory_models(request):
    """Unique model names and their counts"""
    model_counts = Bike.objects.values('model_name').annotate(total=Count('id'))

    return Response({"data": model_counts})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inventory_brands(request):
    """Unique brands and their counts"""
    brand_counts = Bike.objects.values('brand').annotate(total=Count('id'))

    return Response({"data": brand_counts})

