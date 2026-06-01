from django.contrib import admin
from .models import MedicineCategory, Medicine, MedicineBatch, Prescription, PrescriptionItem, Dispensation, Sale, SaleItem

@admin.register(MedicineCategory)
class MedicineCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'unit', 'selling_price', 'reorder_level', 'is_active']
    list_filter = ['category', 'is_active']
    search_fields = ['name', 'generic_name']

@admin.register(MedicineBatch)
class MedicineBatchAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'batch_number', 'quantity_remaining', 'expiry_date']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'status', 'created_at']

@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    pass

@admin.register(Dispensation)
class DispensationAdmin(admin.ModelAdmin):
    pass

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    pass