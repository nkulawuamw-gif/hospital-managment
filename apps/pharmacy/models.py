from django.db import models
from simple_history.models import HistoricalRecords
from apps.accounts.models import User
from apps.patients.models import Patient
from apps.emr.models import Consultation


class MedicineCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'medicine_categories'

    def __str__(self):
        return self.name


class Medicine(models.Model):
    class Unit(models.TextChoices):
        TABLET = 'tablet', 'Tablet'
        CAPSULE = 'capsule', 'Capsule'
        ML = 'ml', 'ML'
        MG = 'mg', 'MG'
        INJECTION = 'injection', 'Injection'
        SYRUP = 'syrup', 'Syrup'
        CREAM = 'cream', 'Cream'
        DROPS = 'drops', 'Drops'
        OTHER = 'other', 'Other'

    name = models.CharField(max_length=300)
    category = models.ForeignKey(MedicineCategory, on_delete=models.SET_NULL, null=True, related_name='medicines')
    brand = models.CharField(max_length=200, blank=True)
    generic_name = models.CharField(max_length=300, blank=True)
    unit = models.CharField(max_length=20, choices=Unit.choices, default=Unit.TABLET)
    strength = models.CharField(max_length=100, blank=True, help_text='e.g., 500mg')
    packaging = models.CharField(max_length=100, blank=True, help_text='e.g., 100 tablets')
    reorder_level = models.IntegerField(default=10)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    requires_prescription = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        db_table = 'medicines'
        indexes = [
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f'{self.name} ({self.strength})'


class MedicineBatch(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='batches')
    batch_number = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    quantity_remaining = models.IntegerField(default=0)
    manufacturing_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField()
    supplier = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'medicine_batches'
        indexes = [
            models.Index(fields=['expiry_date']),
            models.Index(fields=['batch_number']),
        ]

    def __str__(self):
        return f'{self.medicine.name} - {self.batch_number} (Remaining: {self.quantity_remaining})'

    @property
    def is_expired(self):
        from datetime import date
        return self.expiry_date < date.today()

    @property
    def is_low_stock(self):
        return self.quantity_remaining <= self.medicine.reorder_level


class Prescription(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        DISPENSED = 'dispensed', 'Dispensed'
        PARTIAL = 'partial', 'Partially Dispensed'
        CANCELLED = 'cancelled', 'Cancelled'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prescriptions', limit_choices_to={'role': 'doctor'})
    consultation = models.ForeignKey(Consultation, on_delete=models.SET_NULL, null=True, blank=True, related_name='prescriptions')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_prescriptions')

    history = HistoricalRecords()

    class Meta:
        db_table = 'prescriptions'

    def __str__(self):
        return f'Prescription - {self.patient.patient_id} by Dr. {self.doctor.last_name}'


class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='prescription_items')
    dosage = models.CharField(max_length=200, help_text='e.g., 1 tablet twice daily')
    quantity = models.IntegerField()
    days_supply = models.IntegerField(default=1)
    notes = models.TextField(blank=True)
    is_dispensed = models.BooleanField(default=False)
    quantity_dispensed = models.IntegerField(default=0)

    class Meta:
        db_table = 'prescription_items'

    def __str__(self):
        return f'{self.medicine.name} x {self.quantity}'


class Dispensation(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='dispensations')
    dispensed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='dispensations', limit_choices_to={'role': 'pharmacist'})
    notes = models.TextField(blank=True)
    dispensed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dispensations'

    def __str__(self):
        return f'Dispensation - {self.prescription.patient.patient_id}'


class Sale(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='pharmacy_sales')
    items = models.ManyToManyField(Medicine, through='SaleItem', related_name='sales')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method = models.CharField(max_length=20, default='cash')
    sold_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'pharmacy_sales'

    def __str__(self):
        return f'Sale - {self.patient.patient_id} - {self.total_amount}'


class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'pharmacy_sale_items'
