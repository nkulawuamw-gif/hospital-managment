from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'suppliers', views.SupplierViewSet)
router.register(r'categories', views.SupplyCategoryViewSet)
router.register(r'supplies', views.SupplyViewSet)
router.register(r'purchase-orders', views.PurchaseOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path('web/', views.supply_list, name='supply_list'),
    path('web/create/', views.supply_create, name='supply_create'),
    path('web/<int:pk>/edit/', views.supply_edit, name='supply_edit'),
    path('web/suppliers/', views.supplier_list, name='supplier_list'),
    path('web/suppliers/create/', views.supplier_create, name='supplier_create'),
    path('web/pos/', views.po_list, name='po_list'),
    path('web/pos/create/', views.po_create, name='po_create'),
    path('web/pos/<int:pk>/', views.po_detail, name='po_detail'),
    path('web/pos/<int:pk>/receive/', views.receive_stock, name='receive_stock'),
    path('web/issue/', views.stock_issue, name='stock_issue'),
    path('web/issues/', views.issue_history, name='issue_history'),
]
