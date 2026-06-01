from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DepartmentViewSet, SpecializationViewSet, DoctorProfileViewSet, DoctorScheduleViewSet

router = DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'specializations', SpecializationViewSet)
router.register(r'profiles', DoctorProfileViewSet)
router.register(r'schedules', DoctorScheduleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]