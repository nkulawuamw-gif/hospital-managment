from django.db import models, transaction
from django.db.models import Sum, F
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class PatientVisit(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        COMPLETED = 'completed', 'Completed'
        BILLED = 'billed', 'Billed'
        CANCELLED = 'cancelled', 'Cancelled'

    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE, related_name='visits')
    visit_number = models.CharField(max_length=20, unique=True, editable=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_visits')
    checked_in_at = models.DateTimeField(default=timezone.now)
    checked_out_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'patient_visits'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.visit_number} - {self.patient}'

    def save(self, *args, **kwargs):
        if not self.visit_number:
            today = timezone.now().strftime('%y%m%d')
            last = PatientVisit.objects.filter(visit_number__startswith=f'V{today}') \
                .order_by('visit_number').last()
            if last:
                num = int(last.visit_number[7:]) + 1
            else:
                num = 1
            self.visit_number = f'V{today}{num:04d}'
        super().save(*args, **kwargs)

    @property
    def total_medication_cost(self):
        result = EncounterMedication.objects.filter(
            encounter__visit=self
        ).aggregate(total=Sum(F('unit_price') * F('quantity')))
        return result['total'] or 0

    @property
    def total_items(self):
        return EncounterMedication.objects.filter(encounter__visit=self).count()


class Encounter(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'
        SKIPPED = 'skipped', 'Skipped'

    visit = models.ForeignKey(PatientVisit, on_delete=models.CASCADE, related_name='encounters')
    department = models.ForeignKey('doctors.StaffDepartment', on_delete=models.CASCADE, related_name='encounters')
    referred_from = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals_made')
    referred_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals_given')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    seen_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='encounters_seen')
    chief_complaint = models.TextField(blank=True)
    assessment = models.TextField(blank=True)
    intervention = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'encounters'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.visit.visit_number} @ {self.department.name}'

    @property
    def medication_cost(self):
        result = self.medications.aggregate(total=Sum(F('unit_price') * F('quantity')))
        return result['total'] or 0


class EncounterMedication(models.Model):
    encounter = models.ForeignKey(Encounter, on_delete=models.CASCADE, related_name='medications')
    medicine = models.ForeignKey('pharmacy.Medicine', on_delete=models.CASCADE, related_name='encounter_medications')
    quantity = models.PositiveIntegerField()
    dosage = models.CharField(max_length=200, blank=True, help_text='e.g., 1 tablet twice daily')
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    is_dispensed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'encounter_medications'

    def __str__(self):
        return f'{self.medicine.name} x {self.quantity}'
