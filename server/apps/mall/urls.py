from django.urls import path, include
from rest_framework import routers

from .views import ProductViewSet, OrderViewSet, PaymentRecordViewSet

router = routers.DefaultRouter()
router.register('product', ProductViewSet, basename='product')
router.register('order', OrderViewSet, basename='order')
router.register('pay_record', PaymentRecordViewSet, basename='pay_record')
urlpatterns = [
    path('', include(router.urls)),
]
