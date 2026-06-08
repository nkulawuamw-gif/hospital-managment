from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.MedicineCategoryViewSet)
router.register(r'medicines', views.MedicineViewSet)
router.register(r'batches', views.MedicineBatchViewSet)
router.register(r'prescriptions', views.PrescriptionViewSet)
router.register(r'prescription-items', views.PrescriptionItemViewSet)
router.register(r'dispensations', views.DispensationViewSet)
router.register(r'sales', views.SaleViewSet)

urlpatterns = [
    path('', include(router.urls)),

    # Template views
    path('web/', views.medicine_list, name='medicines'),
    path('web/create/', views.medicine_create, name='medicine_create'),
    path('web/<int:pk>/edit/', views.medicine_edit, name='medicine_edit'),
    path('web/batches/', views.batch_list, name='batches'),
    path('web/batches/create/', views.batch_create, name='batch_create'),
    path('web/prescriptions/', views.prescription_list, name='prescriptions'),
    path('web/prescriptions/<int:pk>/', views.prescription_detail, name='prescription_detail'),
    path('web/prescriptions/<int:pk>/dispense/', views.prescription_dispense, name='prescription_dispense'),

    # Sale POS
    path('web/sales/', views.sale_list, name='sale_list'),
    path('web/sales/create/', views.sale_create, name='sale_create'),
    path('web/sales/<int:pk>/', views.sale_detail, name='sale_detail'),

    # Dispensation history
    path('web/dispensations/', views.dispensation_list, name='dispensation_list'),
]
