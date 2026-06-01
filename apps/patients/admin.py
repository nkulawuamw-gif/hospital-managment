from django.contrib import admin
from .models import Patient, MedicalHistory


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['patient_id', 'full_name', 'gender', 'phone', 'blood_group', 'is_active']
    list_filter = ['gender', 'blood_group', 'is_active']
    search_fields = ['patient_id', 'first_name', 'last_name', 'phone', 'national_id']
    list_per_page = 25


@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ['patient', 'condition', 'diagnosed_date']
