from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WardViewSet, BedViewSet, AdmissionViewSet, TransferViewSet

router = DefaultRouter()
router.register(r'wards', WardViewSet)
router.register(r'beds', BedViewSet)
router.register(r'admissions', AdmissionViewSet)
router.register(r'transfers', TransferViewSet)

urlpatterns = [
    path('', include(router.urls)),
]