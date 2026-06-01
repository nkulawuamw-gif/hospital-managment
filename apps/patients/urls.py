from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.PatientViewSet)
router.register(r'medical-histories', views.MedicalHistoryViewSet)

urlpatterns = [
    # Template views (must come before API to avoid pk="web" matching)
    path('web/', views.patient_list, name='list'),
    path('web/create/', views.patient_create, name='create'),
    path('web/<int:pk>/', views.patient_detail, name='detail'),
    path('web/<int:pk>/edit/', views.patient_edit, name='edit'),

    # API
    path('', include(router.urls)),
]
