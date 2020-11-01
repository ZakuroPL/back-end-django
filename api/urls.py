from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import ProductViewSet, LocationViewSet, TransferViewSet, UserViewSet, HistoryViewSet, \
    HistoryOfLoginToZakuroViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('products', ProductViewSet)
router.register('locations', LocationViewSet)
router.register('transfers', TransferViewSet)
router.register('history', HistoryViewSet)

router.register('login-history', HistoryOfLoginToZakuroViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
