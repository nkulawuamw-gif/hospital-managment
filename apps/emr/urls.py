from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'icd-codes', views.ICDCodeViewSet)
router.register(r'consultations', views.ConsultationViewSet)
router.register(r'soap-notes', views.SOAPNoteViewSet)
router.register(r'attachments', views.AttachmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('web/', views.consultation_list, name='list'),
    path('web/create/', views.consultation_create, name='create'),
    path('web/<int:pk>/', views.consultation_detail, name='detail'),
]
