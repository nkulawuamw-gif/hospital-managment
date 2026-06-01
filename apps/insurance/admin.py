from django.contrib import admin
from .models import InsuranceCompany, PatientInsurance, InsuranceClaim

@admin.register(InsuranceCompany)
class InsuranceCompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'coverage_percentage', 'is_active']

@admin.register(PatientInsurance)
class PatientInsuranceAdmin(admin.ModelAdmin):
    list_display = ['patient', 'insurance_company', 'policy_number', 'is_active']

@admin.register(InsuranceClaim)
class InsuranceClaimAdmin(admin.ModelAdmin):
    list_display = ['claim_number', 'patient', 'amount_claimed', 'status']
    list_filter = ['status']