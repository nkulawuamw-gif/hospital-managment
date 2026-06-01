from django.contrib import admin
from .models import LabTestCategory, LabTest, LabTestParameter, LabRequest, LabRequestItem, LabResultParameter

@admin.register(LabTestCategory)
class LabTestCategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_active']

@admin.register(LabTestParameter)
class LabTestParameterAdmin(admin.ModelAdmin):
    pass

@admin.register(LabRequest)
class LabRequestAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'priority', 'status', 'created_at']
    list_filter = ['status', 'priority']

@admin.register(LabRequestItem)
class LabRequestItemAdmin(admin.ModelAdmin):
    pass

@admin.register(LabResultParameter)
class LabResultParameterAdmin(admin.ModelAdmin):
    pass