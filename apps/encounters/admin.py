from django.contrib import admin
from .models import PatientVisit, Encounter, EncounterMedication


class EncounterInline(admin.TabularInline):
    model = Encounter
    extra = 0
    readonly_fields = ['department', 'status', 'seen_by', 'intervention']


class EncounterMedicationInline(admin.TabularInline):
    model = EncounterMedication
    extra = 0
    readonly_fields = ['unit_price', 'total_price']


@admin.register(PatientVisit)
class PatientVisitAdmin(admin.ModelAdmin):
    list_display = ['visit_number', 'patient', 'status', 'total_medication_cost', 'created_at']
    list_filter = ['status']
    search_fields = ['visit_number', 'patient__first_name', 'patient__last_name', 'patient__patient_id']
    readonly_fields = ['visit_number', 'total_medication_cost']
    inlines = [EncounterInline]


@admin.register(Encounter)
class EncounterAdmin(admin.ModelAdmin):
    list_display = ['visit', 'department', 'status', 'seen_by', 'medication_cost', 'created_at']
    list_filter = ['status', 'department']
    search_fields = ['visit__visit_number', 'department__name']
    inlines = [EncounterMedicationInline]


@admin.register(EncounterMedication)
class EncounterMedicationAdmin(admin.ModelAdmin):
    list_display = ['encounter', 'medicine', 'quantity', 'unit_price', 'total_price', 'is_dispensed']
    list_filter = ['is_dispensed']
