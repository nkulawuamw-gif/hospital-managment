from django.db import models
from simple_history.models import HistoricalRecords
from apps.accounts.models import User
from apps.patients.models import Patient


class InsuranceCompany(models.Model):
    name = models.CharField(max_length=200, unique=True)
    code = models.CharField(max_length=50, unique=True)
    contact_person = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    coverage_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=80, help_text='Default coverage %')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'insurance_companies'

    def __str__(self):
        return self.name


class PatientInsurance(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='insurance_policies')
    insurance_company = models.ForeignKey(InsuranceCompany, on_delete=models.CASCADE, related_name='policies')
    policy_number = models.CharField(max_length=100)
    coverage_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=80)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'patient_insurance'

    def __str__(self):
        return f'{self.patient.patient_id} - {self.insurance_company.name}'


class InsuranceClaim(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        SUBMITTED = 'submitted', 'Submitted'
        APPROVED = 'approved', 'Approved'
        REJECTED = 'rejected', 'Rejected'
        PAID = 'paid', 'Paid'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='insurance_claims')
    insurance_policy = models.ForeignKey(PatientInsurance, on_delete=models.CASCADE, related_name='claims')
    invoice = models.ForeignKey('billing.Invoice', on_delete=models.SET_NULL, null=True, blank=True, related_name='insurance_claims')
    claim_number = models.CharField(max_length=50, unique=True)
    amount_claimed = models.DecimalField(max_digits=12, decimal_places=2)
    amount_approved = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    notes = models.TextField(blank=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='submitted_claims')
    submitted_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_claims')
    approved_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        db_table = 'insurance_claims'

    def __str__(self):
        return f'Claim {self.claim_number} - {self.patient.patient_id}'
