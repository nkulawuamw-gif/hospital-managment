from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'wards', views.WardViewSet)
router.register(r'beds', views.BedViewSet)
router.register(r'admissions', views.AdmissionViewSet)
router.register(r'transfers', views.TransferViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Wards
    path('web/wards/', views.ward_list, name='wards'),
    path('web/wards/create/', views.ward_create, name='ward_create'),
    path('web/wards/<int:pk>/edit/', views.ward_edit, name='ward_edit'),

    # Admissions
    path('web/admissions/', views.admission_list, name='admissions'),
    path('web/admissions/create/', views.admission_create, name='admission_create'),
    path('web/admissions/<int:pk>/', views.admission_detail, name='admission_detail'),
    path('web/admissions/<int:pk>/transfer/', views.admission_transfer, name='admission_transfer'),
    path('web/admissions/<int:pk>/discharge/', views.admission_discharge, name='admission_discharge'),
]
