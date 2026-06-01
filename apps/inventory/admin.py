from django.contrib import admin
from .models import Supplier, SupplyCategory, Supply, PurchaseOrder, PurchaseOrderItem, StockReceiving, StockIssue, StockIssueItem

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'is_active']

@admin.register(SupplyCategory)
class SupplyCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'current_stock', 'reorder_level', 'is_active']

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'supplier', 'status', 'total_amount']

@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    pass