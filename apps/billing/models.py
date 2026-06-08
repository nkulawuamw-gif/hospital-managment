from django.db import models
from simple_history.models import HistoricalRecords
from apps.accounts.models import User
from apps.patients.models import Patient
from apps.appointments.models import Appointment
from apps.inpatient.models import Admission


class Invoice(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'
        PARTIAL = 'partial', 'Partially Paid'
        CANCELLED = 'cancelled', 'Cancelled'
        OVERDUE = 'overdue', 'Overdue'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=20, unique=True)
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    admission = models.ForeignKey(Admission, on_delete=models.SET_NULL, null=True, blank=True, related_name='invoices')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issued_invoices')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        db_table = 'invoices'
        indexes = [
            models.Index(fields=['invoice_number']),
            models.Index(fields=['status']),
            models.Index(fields=['patient']),
        ]

    def __str__(self):
        return f'Invoice {self.invoice_number} - {self.patient.patient_id}'


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=300)
    medicine = models.ForeignKey(
        'pharmacy.Medicine', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='invoice_items',
        help_text='Linked inventory item if the line was picked from the medicine list',
    )
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'invoice_items'

    def __str__(self):
        return f'{self.description} x {self.quantity}'


class Payment(models.Model):
    class Method(models.TextChoices):
        CASH = 'cash', 'Cash'
        MOBILE_MONEY = 'mobile_money', 'Mobile Money'
        BANK_TRANSFER = 'bank_transfer', 'Bank Transfer'
        CARD = 'card', 'Card'
        INSURANCE = 'insurance', 'Insurance'

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=Method.choices, default=Method.CASH)
    transaction_reference = models.CharField(max_length=200, blank=True)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='received_payments')
    notes = models.TextField(blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return f'Payment {self.transaction_reference} - {self.amount}'


class Quotation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='quotations')
    items = models.JSONField(default=list, help_text='List of quoted items/services')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    valid_until = models.DateField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'quotations'
