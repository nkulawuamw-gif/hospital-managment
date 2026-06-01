from django.db import models
from simple_history.models import HistoricalRecords
from apps.accounts.models import User
from apps.patients.models import Patient
from apps.appointments.models import Appointment


class LabTestCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        db_table = 'lab_test_categories'

    def __str__(self):
        return self.name


class LabTest(models.Model):
    name = models.CharField(max_length=300)
    category = models.ForeignKey(LabTestCategory, on_delete=models.SET_NULL, null=True, related_name='tests')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    turnaround_time = models.CharField(max_length=100, blank=True, help_text='e.g., 2-3 hours')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lab_tests'

    def __str__(self):
        return self.name


class LabTestParameter(models.Model):
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE, related_name='parameters')
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50, blank=True)
    normal_range_min = models.CharField(max_length=50, blank=True)
    normal_range_max = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'lab_test_parameters'

    def __str__(self):
        return f'{self.test.name} - {self.name}'


class LabRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SAMPLE_COLLECTED = 'sample_collected', 'Sample Collected'
        PROCESSING = 'processing', 'Processing'
        COMPLETED = 'completed', 'Completed'
        APPROVED = 'approved', 'Approved'
        CANCELLED = 'cancelled', 'Cancelled'

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_requests')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lab_requests', limit_choices_to={'role': 'doctor'})
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='lab_requests')
    tests = models.ManyToManyField(LabTest, through='LabRequestItem', related_name='requests')
    priority = models.CharField(max_length=20, choices=[('routine', 'Routine'), ('urgent', 'Urgent'), ('stat', 'STAT')], default='routine')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    clinical_notes = models.TextField(blank=True)
    sample_collected_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='collected_samples')
    sample_collected_at = models.DateTimeField(null=True, blank=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_tests')
    processed_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_tests')
    approved_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        db_table = 'lab_requests'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f'Lab Request - {self.patient.patient_id}'


class LabRequestItem(models.Model):
    lab_request = models.ForeignKey(LabRequest, on_delete=models.CASCADE)
    test = models.ForeignKey(LabTest, on_delete=models.CASCADE)
    result = models.TextField(blank=True)
    is_abnormal = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    result_file = models.FileField(upload_to='lab_results/', blank=True, null=True)

    class Meta:
        db_table = 'lab_request_items'

    def __str__(self):
        return f'{self.lab_request.patient.patient_id} - {self.test.name}'


class LabResultParameter(models.Model):
    request_item = models.ForeignKey(LabRequestItem, on_delete=models.CASCADE, related_name='parameter_results')
    parameter = models.ForeignKey(LabTestParameter, on_delete=models.CASCADE)
    value = models.CharField(max_length=200)
    is_abnormal = models.BooleanField(default=False)

    class Meta:
        db_table = 'lab_result_parameters'

    def __str__(self):
        return f'{self.parameter.name}: {self.value}'
