from django.contrib import admin
from .models import StaffDepartment, Specialization, DoctorProfile, DoctorSchedule

@admin.register(StaffDepartment)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'is_active']

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'license_number', 'consultation_fee', 'is_available']
    list_filter = ['department', 'is_available']

@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'from_time', 'to_time', 'is_available']