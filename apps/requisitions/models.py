from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords


class Requisition(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending Approval'
        APPROVED = 'approved', 'Approved'
        PROCESSING = 'processing', 'Processing'
        DISPATCHED = 'dispatched', 'Dispatched & Confirmed'
        REJECTED = 'rejected', 'Rejected'
        CANCELLED = 'cancelled', 'Cancelled'

    request_number = models.CharField(max_length=20, unique=True)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requisitions')
    department = models.ForeignKey('doctors.StaffDepartment', on_delete=models.SET_NULL, null=True, blank=True, related_name='requisitions')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)

    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_requisitions')
    approved_at = models.DateTimeField(null=True, blank=True)
    approval_notes = models.TextField(blank=True)

    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_requisitions')
    processed_at = models.DateTimeField(null=True, blank=True)

    dispatched_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='dispatched_requisitions')
    dispatched_at = models.DateTimeField(null=True, blank=True)
    dispatch_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        db_table = 'requisitions'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.request_number} ({self.get_status_display()})'


class RequisitionItem(models.Model):
    requisition = models.ForeignKey(Requisition, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey('pharmacy.Medicine', on_delete=models.CASCADE, null=True, blank=True)
    quantity_requested = models.PositiveIntegerField()
    quantity_approved = models.PositiveIntegerField(null=True, blank=True)
    quantity_delivered = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    class Meta:
        db_table = 'requisition_items'

    def __str__(self):
        med = self.medicine.name if self.medicine else 'Unknown'
        return f'{med} x{self.quantity_requested}'
