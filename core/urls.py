from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import CustomerViewSet, BikeViewSet, StorageViewSet, OrderViewSet, CustomerOrdersList

router = routers.DefaultRouter()
router.register('customers', CustomerViewSet, basename="Customers")
router.register('inventory', BikeViewSet, basename="Inventory")
router.register('storage', StorageViewSet, basename="Storage")
router.register('order', OrderViewSet, basename="Order")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("customers/<int:pk>/orders/", CustomerOrdersList.as_view()),
]
