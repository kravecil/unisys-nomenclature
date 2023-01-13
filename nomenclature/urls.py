from django.urls import path, include

from .views import *
from rest_framework.routers import DefaultRouter

app_name = 'nomenclature'

router = DefaultRouter()
router.register(r'requests', RequestViewSet)
router.register(r'products', ProductViewSet)
router.register(r'units', UnitViewSet)
router.register(r'okpds', OkpdViewSet)
router.register(r'okveds', OkvedViewSet)
router.register(r'enses', EnsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]

