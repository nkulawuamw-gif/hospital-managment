from django.contrib import admin
from .models import Ward, Bed, Admission, Transfer

@admin.register(Ward)
class WardAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'capacity', 'charge_per_day', 'is_active']

@admin.register(Bed)
class BedAdmin(admin.ModelAdmin):
    list_display = ['ward', 'bed_number', 'is_occupied']
    list_filter = ['is_occupied', 'ward']

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'ward', 'bed', 'doctor', 'status', 'admission_date']
    list_filter = ['status']

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    pass