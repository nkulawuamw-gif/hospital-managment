from django.contrib import admin
from .models import Appointment, AppointmentReminder

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'doctor', 'appointment_date', 'appointment_time', 'status']
    list_filter = ['status', 'appointment_date']
    search_fields = ['patient__patient_id', 'patient__first_name', 'doctor__email']

@admin.register(AppointmentReminder)
class AppointmentReminderAdmin(admin.ModelAdmin):
    pass