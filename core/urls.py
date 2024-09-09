from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import CustomerViewSet, UsersViewset, BikeViewSet, StorageViewSet, OrderViewSet, CustomerOrdersList, StorageTransferList, GiftViewSet

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from api.views import ReportsView

router = routers.DefaultRouter()
router.register('customers', CustomerViewSet, basename="Customers")
router.register('inventory', BikeViewSet, basename="Inventory")
router.register('storage', StorageViewSet, basename="Storage")
router.register('order', OrderViewSet, basename="Order")
router.register('employees', UsersViewset, basename="Employees")
router.register('gifts', GiftViewSet, basename="Gifts")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),

    path("customers/<int:pk>/orders/", CustomerOrdersList.as_view()),
    path("storage/transfer/history/", StorageTransferList.as_view()),

    path("reports/sales/volume", ReportsView.sales_volume, name='sales_volume'),
    path("reports/sales/payment_method", ReportsView.sales_payment_method, name='sales_payment_method'),

    path("reports/inventory/volume", ReportsView.inventory_volume, name='inventory_volume'),
    path("reports/inventory/brands", ReportsView.inventory_brands, name="brands_report"),
    path("reports/inventory/models", ReportsView.inventory_models, name="models_report"),
    path("reports/inventory/storages", ReportsView.inventory_storages, name="storages_report"),

    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
