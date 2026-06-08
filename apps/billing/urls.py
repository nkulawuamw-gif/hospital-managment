from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'invoices', views.InvoiceViewSet)
router.register(r'invoice-items', views.InvoiceItemViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'quotations', views.QuotationViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('web/', views.invoice_list, name='invoice_list'),
    path('web/create/', views.invoice_create, name='invoice_create'),
    path('web/<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('web/<int:pk>/pay/', views.record_payment, name='record_payment'),
    path('web/quotations/', views.quotation_list, name='quotation_list'),
    path('web/quotations/create/', views.quotation_create, name='quotation_create'),
    path('api/medicines/', views.medicines_api, name='medicines_api'),
]
