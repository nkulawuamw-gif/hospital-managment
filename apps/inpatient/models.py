from django.db import models
from simple_history.models import HistoricalRecords
from apps.accounts.models import User
from apps.patients.models import Patient
from apps.doctors.models import Department


class Ward(models.Model):
    class Type(models.TextChoices):
        GENERAL = 'general', 'General Ward'
        PRIVATE = 'private', 'Private Room'
        ICU = 'icu', 'ICU'
        MATERNITY = 'maternity', 'Maternity'
        PEDIATRIC = 'pediatric', 'Pediatric'
        EMERGENCY = 'emergency', 'Emergency'

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.GENERAL)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    floor = models.CharField(max_length=50, blank=True)
    capacity = models.IntegerField(default=10)
    charge_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'wards'

    def __str__(self):
        return self.name

    @property
    def available_beds(self):
        return self.capacity - self.beds.filter(is_occupied=True).count()


class Bed(models.Model):
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=20)
    is_occupied = models.BooleanField(default=False)

    class Meta:
        db_table = 'beds'
        unique_together = ['ward', 'bed_number']

    def __str__(self):
        return f'{self.ward.name} - Bed {self.bed_number}'


class Admission(models.Model):
    class Status(models.TextChoices):
        ADMITTED = 'admitted', 'Admitted'
        TRANSFERRED = 'transferred', 'Transferred'
        DISCHARGED = 'discharged', 'Discharged'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='admissions')
    ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, related_name='admissions')
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True, related_name='admissions')
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='admissions', limit_choices_to={'role': 'doctor'})
    diagnosis = models.TextField()
    admission_date = models.DateTimeField(auto_now_add=True)
    discharge_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ADMITTED)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_admissions')

    history = HistoricalRecords()

    class Meta:
        db_table = 'admissions'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['admission_date']),
        ]

    def __str__(self):
        return f'Admission - {self.patient.patient_id} ({self.get_status_display()})'


class Transfer(models.Model):
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE, related_name='transfers')
    from_ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, related_name='transfers_from')
    to_ward = models.ForeignKey(Ward, on_delete=models.SET_NULL, null=True, related_name='transfers_to')
    from_bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True, related_name='transfers_from')
    to_bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True, related_name='transfers_to')
    reason = models.TextField()
    transferred_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    transferred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transfers'

    def __str__(self):
        return f'Transfer - {self.admission.patient.patient_id}'
